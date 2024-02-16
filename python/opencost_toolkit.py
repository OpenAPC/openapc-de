#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from collections import OrderedDict

import re
import xml.etree.ElementTree as ET

import openapc_toolkit as oat

OPENCOST_EXTRACTION_FIELDS = OrderedDict([
    ("institution_ror", "opencost:institution//opencost:institution_id[@type='ror']"),
    ("period", None),
    ("euro", None),
    ("doi", "opencost:primary_identifier//opencost:doi"),
    ("is_hybrid", None),
    ("type", "opencost:type"),
    ("contract_primary_identifier", None),
    ("contract_invoice_id", None),
    ("gold-oa", None),
    ("vat", None),
    ("colour charge", None),
    ("cover charge", None),
    ("hybrid-oa", None),
    ("other", None),
    ("page charge", None),
    ("permission", None),
    ("publication charge", None),
    ("reprint", None),
    ("submission fee", None),
    ("payment fee", None),
])

def _process_oc_invoice_data(invoice_element, namespaces, strict_vat=True):
    """
    Extract and process payment data from an openCost invoice element.
    """
    global EXCHANGE_RATES

    msgs = {
        'conv_no_period': 'Automated conversion to EUR failed - no period ' +
                          'value found.',
        'conv_failed': 'Automated conversion to EUR failed - {}',
        'conv_no_rate': 'Automated conversion to EUR failed - No annual ' +
                        'exchange rate available for currency {} and period {}.',
        'multiple_vats': 'Encountered more than one cost_type "vat". Data ' +
                         'might be ambiguous, please check manually. ',
        'add_amounts_paid': 'Cost type {} occurs more than once in the same ' +
                       'invoice, adding amounts ({} + {} = {})'
    }

    cost_data_xpaths = {
        "date_paid": "opencost:dates//opencost:date_paid",
        "date_invoice": "opencost:dates//opencost:date_invoice",
        # Extract dates before cost data as we may need them for currency conversion
        "amount_paid": "opencost:amounts_paid//opencost:amount_paid"
    }
    ret = {
        "success": False,
        "data": None,
        "error_msg": None
    }
    data = {}
    for field, xpath in cost_data_xpaths.items():
        results = invoice_element.findall(xpath, namespaces)
        for result in results:
            if result is None or result.text is None:
                continue
            # Apply processing rules depending on field type
            if field in ["date_paid", "date_invoice"]:
                target_field = field
                if re.match(r"\d{4}-[0-1]{1}\d(-[0-3]{1}\d)?", result.text):
                    value = result.text[:4]
                else:
                    value = result.text
            elif field == "amount_paid":
                cur = result.attrib["currency"]
                cost_type = result.attrib["type"]
                value = oat._auto_atof(result.text)
                if cur != "EUR":
                    if "date_paid" in data:
                        period = data["date_paid"]
                    elif "date_invoice" in data:
                        period = data["date_invoice"]
                    else:
                        ret["error_msg"] = msgs["conv_no_period"]
                        return ret
                    if cur not in EXCHANGE_RATES:
                        try:
                            EXCHANGE_RATES[cur] = get_euro_exchange_rates(cur, "A")
                        except ValueError as ve:
                            ret["error_msg"] = msgs["conv_failed"].format(str(ve))
                            return ret
                    try:
                        exchange_rate = EXCHANGE_RATES[cur][period]
                    except KeyError as ke:
                        ret["error_msg"] = msgs["conv_no_rate"].format(cur, period)
                        return ret
                    euro_value = round(value/float(exchange_rate), 2)
                    msg = 'Automated conversion: {} {} -> {} EUR (period: {})'
                    msg = msg.format(value, cur, euro_value, period)
                    oat.print_c(msg)
                    value = euro_value
                # Add monetary values of the same cost type
                target_field = cost_type
                if target_field in data:
                    # special case VAT, needs to be solved later
                    if target_field == 'vat' and strict_vat:
                        ret["error_msg"] = msgs["multiple_vats"]
                        return ret
                    old_value = data[target_field]
                    msg = msgs["add_amounts_paid"]
                    msg = msg.format(target_field, old_value, value, old_value + value)
                    oat.print_c(msg)
                    value = old_value + value
            data[target_field] = value
    ret["success"] = True
    ret["data"] = data
    return ret

def _process_oc_contract_cost_data(cost_data_element, namespaces):
    """
    Process and extract invoice data from opencost contract cost_data elements
    """

    msgs = {
        "from_to_diff": "Invoice '{}': Different period values in 'from' " +
                        "and 'to' fields, could not determine an invoice " +
                        "period ({} vs {}).",
        "no_invoice_id": "A contract invoice has no invoice_id (data dump: {}).",
        "from_or_to_missing": "Invoice '{}': The 'from' or 'to' element " +
                              "is missing (or both).",
        "date_invoice_only": "Warning: Period for invoice '{}' could only " +
                             "be inferred from the date_invoice element, which " +
                             "might be inaccurate (should be extracted from " +
                             "'from' and 'to instead')"
    }

    invoice_xpaths = {
        "invoice_id": "opencost:invoice_id",
        "from": "opencost:invoice_period//opencost:from",
        "to": "opencost:invoice_period//opencost:to",
        "date_invoice": "opencost:dates//opencost:date_invoice"
    }

    ret = {
        "success": False,
        "data": None,
        "error_msg": None
    }

    extracted_invoices = []

    invoice_elements = cost_data_element.findall("opencost:invoice", namespaces)
    for invoice_element in invoice_elements:
        processed_invoice = _process_oc_invoice_data(invoice_element, namespaces, strict_vat=False)
        if not processed_invoice["success"]:
            return processed_invoice
        data = processed_invoice["data"]
        for field, xpath in invoice_xpaths.items():
            results = invoice_element.findall(xpath, namespaces)
            for result in results:
                if result is None or result.text is None:
                    continue
                # Apply processing rules
                if field in ["from", "to", "date_invoice"]:
                    if re.match(r"\d{4}-[0-1]{1}\d(-[0-3]{1}\d)?", result.text):
                        value = result.text[:4]
                    else:
                        value = result.text
                else:
                    value = result.text
                data[field] = value
        invoice_id = data.get("invoice_id")
        if invoice_id is None or not oat.has_value(invoice_id):
            msg = msgs["no_invoice_id"].format(data)
            ret["error_msg"] = msg
            return ret
        data["invoice_total"] = 0
        for field, value in data.items():
             # sum all payment amounts
            if field in ["read", "publishing", "vat"]:
                data["invoice_total"] += value
        if "from" in data and "to" in data:
            if data["from"] == data["to"]:
                data["invoice_period"] = data["from"]
            else:
                msg = msgs["from_to_diff"].format(invoice_id, data["from"], data["to"])
                ret["error_msg"] = msg
                return ret
        elif "date_invoice" in data:
            msg = msgs["date_invoice_only"]
            oat.print_y(msg.format(invoice_id))
            data["invoice_period"] = data["date_invoice"]
        else:
            msg = msgs["from_or_to_missing"].format(invoice_id)
            ret["error_msg"] = msg
            return ret
        extracted_invoices.append(data)
    ret["success"] = True
    ret["data"] = extracted_invoices
    return ret

def process_opencost_xml(*xml_content_strings):
    """
    Extract OpenAPC compatible field content from openCost XML

    Take strings containing XML (which should validate against the
    openCost XML schema) and extract a list of dicts representing
    the extracted publication metadata.

    Note that openCost XML may contain both data on publications and
    agreements ("publication" and "contract"). This method will extract
    both and calculate cost data/periods for publications published
    under an agreement using the invoice id.
    """
    namespaces = {
        "opencost": "https://opencost.de"
    }

    record_xpath = "opencost:publication"
    contract_xpath = "opencost:contract"
    cost_data_xpath = "opencost:cost_data"

    extracted_records = []
    extracted_invoices = []

    for xml_content in xml_content_strings:
        root = ET.fromstring(xml_content)
        records = root.findall(record_xpath, namespaces)
        for record in records:
            publication = {}
            for field, xpath in OPENCOST_EXTRACTION_FIELDS.items():
                publication[field] = "NA"
                if xpath is not None:
                    result = record.find(xpath, namespaces)
                    if result is not None and result.text is not None:
                        publication[field] = result.text
            cost_data_element = record.find(cost_data_xpath, namespaces)
            cost_data_extract = _process_oc_publication_cost_data(cost_data_element, namespaces)
            if not cost_data_extract["success"]:
                prefix = "Error: "
                if "doi" in publication:
                    prefix = "Error (" +  publication["doi"] + "): "
                print_r(prefix + cost_data_extract["error_msg"])
                extracted_records.append({field: "" for field, _ in OPENCOST_EXTRACTION_FIELDS.items()})
                continue
            for field, value in cost_data_extract["data"].items():
                if field in publication:
                    publication[field] = value
            extracted_records.append(publication)

        contracts = root.findall(contract_xpath, namespaces)
        for contract in contracts:
            cost_data_element = contract.find(cost_data_xpath, namespaces)
            invoices_extract = _process_oc_contract_cost_data(cost_data_element, namespaces)
            if not invoices_extract["success"]:
                print_r("Error: " + invoices_extract["error_msg"])
                continue
            extracted_invoices += invoices_extract["data"]

    extracted_records = _apply_contract_data(extracted_records, extracted_invoices)

    return extracted_records

def _process_oc_publication_cost_data(cost_data_element, namespaces):
    """
    Extract date and cost data from an openCost publication cost_data element

    Takes an openCost cost_data element (as ElementTree) and extracts
    both cost data (APCs and additional costs) and a date value. This
    is a complex task as we have to take several preprocessing rules
    into account as well as the possibility of multiple occurrences. The
    whole process consists of 3 steps:

    1) Aggregate date and cost data for each individual invoice, taking
    into account that amount_paid may occur more than once. Convert
    foreign currencies to EUR and format dates to YYYY. Use simple
    addition for identical cost types in case of multi-occurence.
    2) Merge data from all invoices into one data structure. Check
    different dates for compatibility, again add identical
    cost types in case of multi-occurence.
    3) Map extracted values to OpenAPC fields euro, period and is_hybrid

    If the publication was part of a contract, the primary_identifier
    and invoice_id will be extracted as well. In this case, however, the
    final calculation of costs and dates relies on that invoice data and has
    to be resolved on a higher level. Consistency checks will be omitted
    in this case.
    """

    msgs = {
        'date_inconsistent': 'Multiple {} elements encountered, content ' +
                     'differs.',
        'gold_hybrid_mix': 'Encountered cost types "gold-oa" and "hybrid-oa" ' +
                           'for the same publication.',
        'no_date': 'No date value found and the publication is not part ' +
                   'of any contract.',
        'add_amounts_invoices': 'Cost type {} occurs in more than one invoice, ' +
                                'adding amounts ({} + {} = {})'
    }

    part_of_contract_xpaths = {
        "contract_primary_identifier": "opencost:primary_identifier",
        "contract_invoice_id": "opencost:invoice_id"
    }

    ret = {
        "success": False,
        "data": None,
        "error_msg": None
    }

    final_data = {}

    part_of_contract = cost_data_element.find("opencost:part_of_contract", namespaces)
    if part_of_contract is not None:
        for field, xpath in part_of_contract_xpaths.items():
            result = part_of_contract.find(xpath, namespaces)
            if result is None or result.text is None:
                continue
            final_data[field] = result.text

    invoices = cost_data_element.findall("opencost:invoice", namespaces)
    invoices_data = []
    for invoice_element in invoices:
        processed_invoice = _process_oc_invoice_data(invoice_element, namespaces)
        if not processed_invoice["success"]:
            return processed_invoice
        invoices_data.append(processed_invoice["data"])

    for invoice_data in invoices_data:
        # If there are multiple invoices, we have to merge the data in a
        # meaningful way
        for field, value in invoice_data.items():
            if field not in final_data:
                 # If we have not encountered this type of field yet,
                # we can safely add it
                final_data[field] = value
                continue
            # Otherwise we have to apply special rules on how
            # to combine data from multiple invoices
            if field in ["date_paid", "date_invoice"]:
                if value != final_data[field]:
                    msg = msgs["date_inconsistent"].format(field)
                    ret["error_msg"] = msg
                    return ret
            else:
                # Monetary values can be simply added
                msg = msgs["add_amounts_invoices"]
                old_value = final_data[field]
                msg = msg.format(field, old_value, value, old_value + value)
                oat.print_c(msg)
                final_data[field] += value
    # Final consistency checks + hybrid status extraction
    if "gold-oa" in final_data and "hybrid-oa" in final_data:
        ret["error_msg"] = msgs["gold_hybrid_mix"]
        return ret
    if "gold-oa" in final_data:
        final_data["euro"] = final_data["gold-oa"]
        if "vat" in final_data:
            final_data["euro"] += final_data["vat"]
        final_data["is_hybrid"] = "FALSE"
    if "hybrid-oa" in final_data:
        final_data["euro"] = final_data["hybrid-oa"]
        if "vat" in final_data:
            final_data["euro"] += final_data["vat"]
        final_data["is_hybrid"] = "TRUE"
    if "date_paid" in final_data:
        final_data["period"] =  final_data["date_paid"]
    elif "date_invoice" in final_data:
        final_data["period"] =  final_data["date_invoice"]
    elif not "contract_invoice_id" in final_data:
        ret["error_msg"] = msgs["no_date"]
        return ret
    ret["success"] = True
    ret["data"] = final_data
    return ret

def _apply_contract_data(extracted_records, extracted_invoices):

    msgs = {
        "invoice_id_dup": "Error: invoice_id '{}' occurs more than once!",
        "cost_assigned": "Warning: Record ({}) has assigned non-zero " +
                         "costs of type {} (()€), but is also linked " +
                         "to a contract via an invoice_id ({}). Record " +
                         "cost data was kept, please note that this record " +
                         "does not count towards the total number under " +
                         "the specific contract.",
        "no_records": "Warning: No Records were found matching the " +
                      "contract invoice_id '{}'",
        "cost_calculation": "Found {} records linked to invoice_id '{}'. " +
                            "Publication costs of {} € / {} = {} € will be " +
                            "assigned."
    }

    invoice_dict = {}
    for invoice in extracted_invoices:
        invoice_id = invoice["invoice_id"]
        if invoice_id not in invoice_dict:
            invoice_dict[invoice_id] = invoice
        else:
            print_r(msgs["invoice_id_dup"].format(invoice_id))
            sys.exit()
    for invoice_id, invoice in invoice_dict.items():
        record_count = 0
        for record in extracted_records:
            if not oat.has_value(record["contract_invoice_id"]):
                continue
            if record["contract_invoice_id"] != invoice_id:
                continue
            for cost_type in ["gold-oa", "hybrid-oa"]:
                if oat.has_value(record[cost_type]) and record[cost_type] > 0:
                    msg = msgs["cost_assigned"]
                    msg = msg.format(record["doi"], cost_type, 
                                     record[cost_type], invoice_id)
                    oat.print_y(msg)
                    continue
            record_count += 1
            record["target_invoice_id"] = invoice_id
        if record_count == 0:
            msg = msgs["no_records"].format(invoice_id)
            oat.print_y(msg)
            continue
        record_costs = round(invoice["invoice_total"] / record_count, 2)
        msg = msgs["cost_calculation"]
        msg = msg.format(record_count, invoice_id, invoice["invoice_total"],
                         record_count, record_costs)
        oat.print_c(msg)
        for record in extracted_records:
            if "target_invoice_id" in record and record["target_invoice_id"] == invoice_id:
                record["euro"] = record_costs
                record["period"] = invoice["invoice_period"]
                # DEAL - might need adjustments for other TAs.
                record["is_hybrid"] = "TRUE"
                del(record["target_invoice_id"])
    return extracted_records
