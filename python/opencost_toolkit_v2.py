#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from collections import OrderedDict

import logging
import os
import re
import sys

from io import StringIO
from shutil import copyfileobj
from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET

import openapc_toolkit as oat

try:
    from lxml import etree
except ImportError:
    etree = None
    print("WARNING: 3rd party module 'lxml' not found - optional openCost schema validation will not work")

EXCHANGE_RATES = {}

OPENCOST_EXTRACTION_FIELDS = OrderedDict([
    ("institution_ror", "opencost:institution//opencost:id[opencost:type='ror']//opencost:value"),
    ("institution", "opencost:institution//opencost:name[opencost:type='short']//opencost:value"),
    ("period", None),
    ("euro", None),
    ("doi", "opencost:primary_identifier//opencost:doi"),
    ("is_hybrid", None),
    ("opt-out", None),
    ("type", "opencost:publication_type"),
    ("contract_primary_identifier", None),
    ("contract_group_id", None),
    ("external_costsplitting", "opencost:external_costsplitting"),
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
    ("url", None)
])

OPENCOST_CONTRACT_EXTRACTION_FIELDS = OrderedDict([
    ("institution_ror", "opencost:institution//opencost:id[opencost:type='ror']//opencost:value"),
    ("contract_name", "opencost:contract_name"),
    ("contract_id", "opencost:primary_identifier[opencost:type='ESAC']//opencost:value")
])

# Do not quote the values in 'period' and all cost columns
OPENCOST_STANDARD_QUOTEMASK = [
    True,
    True,
    False,
    False,
    True,
    True,
    True,
    True,
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False
]

class OpenCostValidator(object):

    OPENCOST_XSD_URL = "https://raw.githubusercontent.com/opencost-de/opencost/refs/heads/main/doc/opencost.xsd"

    def __init__(self, force_update=False):
        if not os.path.isdir("tempfiles"):
            os.mkdir("tempfiles")
        filename = "tempfiles/opencost.xsd"
        self.download_opencost_xsd(filename, force_update)
        xsd_doc = etree.parse(filename)
        self.schema = etree.XMLSchema(xsd_doc)

    def download_opencost_xsd(self, filename, force_update=False):
        if os.path.isfile(filename) and not force_update:
            msg = "opencost XSD file already found at {}, using existing copy."
            logging.info(msg.format(filename))
            return
        logging.info("Downloading a fresh copy of the openCost XSD file...")
        request = Request(self.OPENCOST_XSD_URL)
        with urlopen(request) as source:
            with open(filename, "wb") as dest:
                copyfileobj(source, dest)
        msg = "...XSD file successfully written to {}!"
        logging.info(msg.format(filename))

    def validate_xml(self, xml_string):
        ret = {
            "success": True,
            "error_msg": None
        }
        xml = StringIO(xml_string)
        xml_doc = etree.parse(xml)
        try:
            self.schema.assertValid(xml_doc)
            return ret
        except etree.DocumentInvalid as invalid:
            ret["success"] = False
            ret["error_msg"] = str(invalid)
            return ret

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
        'vat_without_costs': 'Encountered a positive vat amount without costs ' +
                             'inside an "amount_paid" element.',
        'both_vat_types': 'Encountered both a vat element inside "amount_paid" ' +
                          'as well as a second "amount_paid" element with cost ' +
                          'type "vat". This type of modeling is ambiguous and not '
                          'recommended.',
        'vat_with_vat': 'An "amount_paid" element with cost_type "vat" should not ' +
                        'have a "vat" sub element.',
        'add_amounts_paid': 'Cost type {} occurs more than once in the same ' +
                       'invoice, adding amounts ({} + {} = {})'
    }

    cost_data_xpaths = {
        "date_paid": "opencost:dates//opencost:paid",
        "date_invoice": "opencost:dates//opencost:invoice",
        # Extract dates before cost data as we may need them for currency conversion
        "amount_paid": "opencost:amounts_paid//opencost:amount_paid"
    }
    ret = {
        "success": False,
        "data": None,
        "error_msg": None,
    }
    local_vat_found = False

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
                cur = result.find("opencost:currency", namespaces).text
                cost_type = result.find("opencost:cost_type", namespaces).text
                amount = result.find("opencost:amount", namespaces).text
                possible_vat = result.find("opencost:vat", namespaces)
                vat_text = None
                if possible_vat is not None:
                    vat_text = possible_vat.text
                value = 0.0
                if amount is not None:
                    value = oat._auto_atof(amount)
                if vat_text is not None:
                    vat_value = oat._auto_atof(vat_text)
                    if value == 0.0 and vat_value > 0.0:
                        ret["error_msg"] = msgs["vat_without_costs"]
                        return ret
                    elif vat_value > 0.0 and cost_type == 'vat':
                        ret["error_msg"] = msgs["vat_with_vat"]
                        return ret
                    else:
                        value += vat_value
                        local_vat_found = True
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
                            EXCHANGE_RATES[cur] = oat.get_euro_exchange_rates(cur, "A")
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
                    logging.info(msg)
                    value = euro_value
                # Add monetary values of the same cost type, handle problematic VAT cases
                target_field = cost_type
                if target_field == 'vat' and local_vat_found:
                    if strict_vat:
                        ret["error_msg"] = msgs["both_vat_types"]
                        return ret
                    else:
                        logging.warning(msgs["both_vat_types"])
                if target_field in data:
                    if target_field == 'vat' and strict_vat:
                        ret["error_msg"] = msgs["multiple_vats"]
                        return ret
                    old_value = data[target_field]
                    msg = msgs["add_amounts_paid"]
                    msg = msg.format(target_field, old_value, value, old_value + value)
                    logging.info(msg)
                    value = old_value + value
            data[target_field] = value
    ret["success"] = True
    ret["data"] = data
    return ret

def _process_oc_contract_cost_data(cost_data_element, namespaces):
    """
    Process and extract invoice groups from opencost contract cost_data elements
    """

    msgs = {
        "from_to_diff": "Group '{}': Different year values in invoices_period " +
                        "'from' and 'to' fields, could not determine a group " +
                        "period ({} vs {}).",
        "date_invoice_only": "Period for invoice '{}' could only " +
                             "be inferred from the date_invoice element, which " +
                             "might be inaccurate (should be extracted from " +
                             "'from' and 'to instead')"
    }

    date_xpaths = {
        "from": "opencost:invoices_period//opencost:from",
        "to": "opencost:invoices_period//opencost:to",
    }

    ret = {
        "success": False,
        "data": None,
        "error_msg": None
    }

    extracted_invoice_groups = []

    group_elements = cost_data_element.findall("opencost:invoice_group", namespaces)
    for group_element in group_elements:
        data = {
            "group_total_costs": 0,
            "invoices": [],
            "merged": False,
            "possible_duplicate": False
        }
        data["group_id"] = group_element.find("opencost:group_id", namespaces).text
        # extract and check the group period
        years = {}
        for field, xpath in date_xpaths.items():
            result = group_element.find(xpath, namespaces)
            if re.match(r"\d{4}-[0-1]{1}\d(-[0-3]{1}\d)?", result.text):
                value = result.text[:4]
            else:
                value = result.text
            years[field] = value
        if years["from"] != years["to"]:
            msg = msgs["from_to_diff"].format(data["group_id"], years["from"], years["to"])
            ret["error_msg"] = msg
            return ret
        else:
            data["period"] = years["from"]
        invoice_elements = group_element.findall("opencost:invoice", namespaces)
        for invoice_element in invoice_elements:
            processed_invoice = _process_oc_invoice_data(invoice_element, namespaces, strict_vat=False)
            if not processed_invoice["success"]:
                return processed_invoice
            invoice_data = processed_invoice["data"]
            for field, value in invoice_data.items():
                 # sum all payment amounts
                if field in ["read", "publish", "vat"]:
                    data["group_total_costs"] += value
            data["invoices"].append(invoice_data)
        extracted_invoice_groups.append(data)
    ret["success"] = True
    ret["data"] = extracted_invoice_groups
    return ret

def process_opencost_oai_records(processing_instructions=None, validate_only=False, force_update=False, record_url=None, *xml_content_strings):
    namespaces = {
        "oai_2_0": "http://www.openarchives.org/OAI/2.0/",
        "opencost": "https://opencost.de"
    }
    record_xpath = ".//oai_2_0:record"
    data_xpath = ".//opencost:data"
    identifier_xpath = ".//oai_2_0:header//oai_2_0:identifier"

    extracted_publications = []
    if validate_only:
        if etree is None:
            logging.critical("Could not import etree. You probably need to install the python lxml package")
            return
        validator = OpenCostValidator(force_update)
        validation_counts = {
            "valid": 0,
            "invalid": 0
        }
    for xml_content in xml_content_strings:
        root = ET.fromstring(xml_content)
        records = root.findall(record_xpath, namespaces)
        for record in records:
            data_element = record.find(data_xpath, namespaces)
            if data_element is None:
                continue
            data_element_xml = ET.tostring(data_element)
            identifier = record.find(identifier_xpath, namespaces)
            if validate_only:
                res = validator.validate_xml(data_element_xml.decode("utf-8"))
                link = identifier.text
                if record_url is not None:
                    link = "[" + record_url + "&identifier=" + identifier.text + "]"
                if res["success"]:
                    msg = "Record {} validates against the openCost schema"
                    logging.info(msg.format(link))
                    validation_counts["valid"] += 1
                else:
                    msg = "Record {} does not validate against the openCost schema: {}"
                    logging.error(msg.format(link, res["error_msg"]))
                    validation_counts["invalid"] += 1
                continue
            publications, _ = process_opencost_xml(data_element_xml)
            for publication in publications: # Should only be one
                publication["identifier"] = identifier.text
                if processing_instructions:
                    target_string = processing_instructions["generator"]
                    for variable in processing_instructions["variables"]:
                        target_string = target_string.replace("%" + variable + "%", publication[variable])
                    publication[processing_instructions["target"]] = target_string
                for key in list(publication.keys()):
                    # postprocessing
                    if publication[key] is not None:
                        publication[key] = str(publication[key])
                        if key == "doi":
                            norm_doi = oat.get_normalised_DOI(publication["doi"])
                            if norm_doi is None:
                                publication["doi"] = "NA"
                            else:
                                publication["doi"] = norm_doi
                        if key == "euro":
                            if not oat.has_value(publication["euro"]):
                                logging.warning("Article skipped, no APC amount found.")
                                break
                            euro_float = oat._auto_atof(publication["euro"])
                            if euro_float is not None and euro_float <= 0.0:
                                msg = "Article skipped, non-positive APC amount found ({})."
                                logging.warning(msg.format(publication['euro']))
                                break
                else:
                    extracted_publications += publications
    if validate_only:
        msg = "Validation run finished.\n valid records: {}\n invalid records: {}"
        oat.print_c(msg.format(validation_counts["valid"], validation_counts["invalid"]))
    return extracted_publications

def process_opencost_xml(*xml_content_strings):
    """
    Extract field content from openCost XML which is relevant to OpenAPC

    Take strings containing XML (which should validate against the
    openCost XML schema) and return a tuple containing a list of
    publication metadata and a list of contract invoice groups.
    """

    msgs = {
        'external_costsplitting': 'Record has been flagged for external costsplitting. ' +
                                  'The cost data probably does not represent the full ' +
                                  'amount OpenAPC is interested in, article was omitted.'
    }

    namespaces = {
        "opencost": "https://opencost.de"
    }
    data_xpath = ".//opencost:data"
    publication_xpath = "opencost:publication"
    contract_xpath = "opencost:contract"
    cost_data_xpath = "opencost:cost_data"


    extracted_publications = []
    extracted_invoice_groups = []

    for xml_content in xml_content_strings:
        logging.debug("Parsing new XML content chunk.")
        root = ET.fromstring(xml_content)
        publications = root.findall(publication_xpath, namespaces)
        logging.info("{} publications extracted.".format(len(publications)))
        for publication in publications:
            publication_data = {}
            for field, xpath in OPENCOST_EXTRACTION_FIELDS.items():
                publication_data[field] = "NA"
                if xpath is not None:
                    result = publication.find(xpath, namespaces)
                    if result is not None and result.text is not None:
                        publication_data[field] = result.text
            if "external_costsplitting" in publication_data:
                if publication_data["external_costsplitting"] in ["1", "true"]:
                    prefix = ""
                    if "doi" in publication_data:
                        prefix += " (" +  publication_data["doi"] + "): "
                    logging.warning(prefix + msgs["external_costsplitting"])
                    extracted_publications.append({field: "" for field, _ in OPENCOST_EXTRACTION_FIELDS.items()})
                    continue
            cost_data_element = publication.find(cost_data_xpath, namespaces)
            cost_data_extract = _process_oc_publication_cost_data(cost_data_element, namespaces)
            if not cost_data_extract["success"]:
                prefix = "Error: "
                if "doi" in publication_data:
                    prefix = "Error (" +  publication_data["doi"] + "): "
                logging.error(prefix + cost_data_extract["error_msg"])
                extracted_publications.append({field: "" for field, _ in OPENCOST_EXTRACTION_FIELDS.items()})
                continue
            for field, value in cost_data_extract["data"].items():
                if field in publication_data:
                    publication_data[field] = value
            extracted_publications.append(publication_data)
        contracts = root.findall(contract_xpath, namespaces)
        logging.info("{} contracts extracted.".format(len(contracts)))
        for contract in contracts:
            contract_data = {}
            for field, xpath in OPENCOST_CONTRACT_EXTRACTION_FIELDS.items():
                contract_data[field] = "NA"
                if xpath is not None:
                    result = contract.find(xpath, namespaces)
                    if result is not None and result.text is not None:
                        contract_data[field] = result.text
            cost_data_element = contract.find(cost_data_xpath, namespaces)
            invoice_groups_extract = _process_oc_contract_cost_data(cost_data_element, namespaces)
            if not invoice_groups_extract["success"]:
                logging.error("Error: " + invoice_groups_extract["error_msg"])
                continue
            invoice_groups = [{**invoice_group, **contract_data} for invoice_group in invoice_groups_extract["data"]]
            extracted_invoice_groups += invoice_groups
    return extracted_publications, extracted_invoice_groups

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
    and invoice group id will be extracted as well. In this case, however, the
    final calculation of costs and dates relies on that invoice data and has
    to be resolved on a higher level. Consistency checks will be omitted
    in this case.
    """

    msgs = {
        'date_inconsistent': 'Multiple "{}" elements encountered, content ' +
                     'differs ({} vs {}) -> Using the earliest date.',
        'gold_hybrid_mix': 'Encountered cost types "gold-oa" and "hybrid-oa" ' +
                           'for the same publication.',
        'no_date': 'No date value found and the publication is not part ' +
                   'of any contract.',
        'add_amounts_invoices': 'Cost type {} occurs in more than one invoice, ' +
                                'adding amounts ({} + {} = {})'
    }

    part_of_contract_xpaths = {
        "contract_primary_identifier": "opencost:primary_identifier/opencost:value",
        "contract_group_id": "opencost:group_id"
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
                    msg = msgs["date_inconsistent"].format(field, value, final_data[field])
                    logging.warning(msg)
                    if value < final_data[field]:
                        final_data[field] = value
            else:
                # Monetary values can be simply added
                msg = msgs["add_amounts_invoices"]
                old_value = final_data[field]
                msg = msg.format(field, old_value, value, old_value + value)
                logging.info(msg)
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
    # Special is_hybrid rule: opt-out
    final_data["opt-out"] = "FALSE"
    esac_id = final_data.get("contract_primary_identifier", "")
    if esac_id:
        if "publication charge" in final_data and not "hybrid-oa" in final_data:
            if final_data["publication charge"] == 0.0:
                final_data["opt-out"] = "TRUE"
                final_data["is_hybrid"] = "TRUE"
                final_data["euro"] = "0.0"
    if "date_paid" in final_data:
        final_data["period"] =  final_data["date_paid"]
    elif "date_invoice" in final_data:
        final_data["period"] =  final_data["date_invoice"]
    elif not "contract_group_id" in final_data:
        ret["error_msg"] = msgs["no_date"]
        return ret
    ret["success"] = True
    ret["data"] = final_data
    return ret

def detect_invoice_group_duplicates(invoice_groups):
    """
    Check a list of invoice group dicts for possible duplicates
    """
    for i in range(len(invoice_groups)):
        group = invoice_groups[i]
        if group["possible_duplicate"]:
            continue
        for j in range(i + 1, len(invoice_groups)):
            comp_group = invoice_groups[j]
            for field in ["group_total_costs", "institution_ror", "period", "contract_id"]:
                if group[field] != comp_group[field]:
                    break
            else:
                group["possible_duplicate"] = True
                comp_group["possible_duplicate"] = True
    return invoice_groups

def merge_invoice_groups(invoice_groups):
    """
    Merge multiple occurences of invoice_groups with the same group_id by adding their total costs

    Given a list of invoice group dicts, this method will search for groups with the same
    group_id and merge them to a single dict by adding their total costs. As a general rule
    invoice groups should not be duplicated in openCost, but certain real world update workflows
    might still end up with group cost data distributed over more than one element/file.
    Note that all merge candidates still have to match in their period, contract_id and institution_ror
    fields, otherwise the method will fail.

    """
    msgs = {
        "merge_error": "Error while trying to merge invoice groups with " +
                       "group_id '{}': The {} field does not match ({} vs {})",
        "merge_info": "Duplicate invoice groups with group_id '{}' were merged, new " +
                      "group total cost is now {} + {} = {}"
    }

    group_dict = {}
    for group in invoice_groups:
        group_id = group["group_id"]
        if group_id not in group_dict:
            group_dict[group_id] = group
            continue
        existing_group = group_dict[group_id]
        for match_field in ["period", "contract_id", "institution_ror"]:
            if existing_group[match_field] != group[match_field]:
                msg = msgs["merge_error"].format(group_id, match_field, existing_group[match_field], group[match_field])
                oat.print_r(msg)
                sys.exit()
        old_costs = group_dict[group_id]["group_total_costs"]
        add_costs = group["group_total_costs"]
        new_costs = old_costs + add_costs
        msg = msgs["merge_info"].format(group_id, old_costs, add_costs, new_costs)
        logging.info(msg)
        group_dict[group_id]["group_total_costs"] = new_costs
        group_dict[group_id]["merged"] = True
        # Keep duplicate hint for merged object
        group_dict[group_id]["possible_duplicate"] = group_dict[group_id]["possible_duplicate"] | group["possible_duplicate"]
    return list(group_dict.values())

def apply_contract_data(extracted_records, extracted_invoice_groups):
    """
    Distribute costs from contract invoice groups over linked publications

    openCost XML may contain both data on publications and
    agreements ("publication" and "contract"). This method will distribute
    cost data/periods for publications published under an agreement using the
    invoice group id. It is meant to work on data returned by process_opencost_xml()
    """

    msgs = {
        "group_id_dup": "Error: group_id '{}' occurs more than once. If this is " +
                        "a confirmed processing artifact, you may want to merge " +
                        "the invoice groups beforehand",
        "cost_assigned": "Record ({}) has assigned non-zero " +
                         "costs of type {} ({}€), but is also linked " +
                         "to a contract via a group_id ({}). Record " +
                         "cost data was kept, please note that this record " +
                         "does not count towards the total number under " +
                         "the specific contract.",
        "no_records": "No Records were found matching the " +
                      "invoice group_id '{}' (contract ID: {})",
        "cost_calculation": "Found {} records linked to group_id '{}'. " +
                            "Publication costs of {} € / {} = {} € will be " +
                            "assigned."
    }
    group_dict = {}
    for group in extracted_invoice_groups:
        group_id = group["group_id"]
        if group_id not in group_dict:
            group_dict[group_id] = group
        else:
            oat.print_r(msgs["group_id_dup"].format(group_id))
            sys.exit()
    for group_id, group in group_dict.items():
        record_count = 0
        for record in extracted_records:
            if not oat.has_value(record["contract_group_id"]):
                continue
            if record["contract_group_id"] != group_id:
                continue
            assigned_costs_found = False
            for cost_type in ["gold-oa", "hybrid-oa"]:
                if record[cost_type] != "NA" and record[cost_type] > 0.0:
                    msg = msgs["cost_assigned"]
                    msg = msg.format(record["doi"], cost_type, 
                                     record[cost_type], group_id)
                    logging.info(msg)
                    assigned_costs_found = True
                    break
            if assigned_costs_found:
                continue
            if record["contract_primary_identifier"] in ["sn2020deal", "wiley2019deal", "els2023deal"]:
                # DEAL special rule: Cost distribution only valid for articles with hybrid_oa == 0€ xor publication charge == 0€. The latter indicates an opt-out article.
                # Might need adjustments for other TAs.
                if not ((record["hybrid-oa"] == 0.0 and record["publication charge"] == 'NA') or (record["hybrid-oa"] == 'NA' and record["publication charge"] == 0.0)):
                    continue
            record_count += 1
            record["target_group_id"] = group_id
        if record_count == 0:
            msg = msgs["no_records"].format(group_id, group["contract_id"])
            logging.warning(msg)
            continue
        record_costs = round(group["group_total_costs"] / record_count, 2)
        msg = msgs["cost_calculation"]
        msg = msg.format(record_count, group_id, group["group_total_costs"],
                         record_count, record_costs)
        logging.info(msg)
        for record in extracted_records:
            if "target_group_id" in record and record["target_group_id"] == group_id:
                record["contract_euro"] = record_costs
                record["period"] = group["period"]
                del(record["target_group_id"])
    return extracted_records
