#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
from datetime import date
from functools import reduce
import json
from math import sqrt, nan
from os import listdir
from subprocess import run
import sys

from babel.dates import format_date
import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "institution": ('The institution to create an analysis for. Must be a designation occuring ' +
                    'in the "institution" column of the core data file'),
    "verbose": "Be more verbose during APC analysis",
    "lang": "The report language"
}

with open("report/strings.json") as f:
    json_content = f.read()
    LANG = json.loads(json_content)

def mean(sample):
    return reduce(lambda x, y: x + y, sample) / len(sample)

def stddev(sample):
    if len(sample) == 1:
        return nan
    mean_value = mean(sample)
    sums = 0.0
    for obs in sample:
        sums += (obs - mean_value)**2
    return sqrt(sums / (len(sample) - 1))

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("institution", help=ARG_HELP_STRINGS["institution"])
    parser.add_argument("lang", help=ARG_HELP_STRINGS["lang"], choices=LANG.keys())
    parser.add_argument("-v", "--verbose", help=ARG_HELP_STRINGS["verbose"], action="store_true")
    return parser.parse_args()

def get_data_dir_stats(data_dir):
    path = "../data/" + data_dir
    files = listdir(path)
    stats = {
        "readme": False,
        "orig_files": 0
    }
    for file_name in files:
        lower = file_name.lower()
        if "readme" in lower:
            stats["readme"] = True
            continue
        if "angereichert" in lower or "enriched" in lower:
            continue
        stats["orig_files"] += 1
    return stats

def generate_header(lang):
    header = LANG[lang]["front"]
    header += LANG[lang]["header"]
    header += LANG[lang]["intro"]
    return header

def generate_metadata_section(institution, ins_content, stats, lang):
    markdown = LANG[lang]["md_header"]
    ins_line = None
    for line in ins_content:
        if line[0] == institution:
            ins_line = line
            break
    else:
        oat.print_r("ERROR: Entry " + institution + " not found in institutions file!")
        sys.exit()
    locale_date = format_date(date.today(), locale=lang)
    markdown += "* " + LANG[lang]["md_date"] + ": " + locale_date + "\n"
    git_rev = run(["git", "describe", "--tags", "--abbrev=0"], capture_output=True).stdout.decode()
    git_rev = git_rev.replace("\n", "")
    rev_url = "https://github.com/OpenAPC/openapc-de/tree/" + git_rev
    markdown += "* " + LANG[lang]["md_rev"] + ": [" + git_rev + "](" + rev_url + ")\n"
    markdown += "* " + LANG[lang]["md_ins"] + ": " + ins_line[2] + "\n"
    markdown += "* " + LANG[lang]["md_ins_apc"] + ": " + ins_line[0] + "\n"
    url = "https://treemaps.intact-project.org/apcdata/"
    treemap_url = "<" + url + ins_line[1].replace("_", "-") + ">"
    markdown += "* " + LANG[lang]["md_treemap"] + ": " + treemap_url + "\n"
    data_dir = ins_line[6]
    if oat.has_value(data_dir):
        stats = get_data_dir_stats(data_dir)
        data_url = "https://github.com/OpenAPC/openapc-de/tree/master/data/" + data_dir
        markdown += "* " + LANG[lang]["md_data_dir"] + ": [" + data_dir + "](" + data_url + ")\n"
        markdown += "* " + LANG[lang]["md_num_files"] +  ": " + str(stats["orig_files"]) + "\n"
        markdown += "* " + LANG[lang]["md_readme"] +  ": "
        if stats["readme"]:
            markdown += LANG[lang]["md_readme_yes"]
        else:
            markdown += LANG[lang]["md_readme_no"]
        markdown += "\n"
    else:
        oat.print_y("WARNING: No data dir entry found for " + institution + "!")
    markdown += "\n"
    return markdown

def generate_duplicates_section(institution, dup_content, ins_content, lang):
    duplicates = {}
    for line in dup_content:
        if line[0] == institution:
            doi = line[3]
            duplicates[doi] = [line]
    if not duplicates:
        return ""
    for line in dup_content:
        doi = line[3]
        if doi in duplicates and line not in duplicates[doi]:
            duplicates[doi].append(line)
    markdown = LANG[lang]["dup_header"]
    markdown += LANG[lang]["dup_intro"]
    markdown += LANG[lang]["dup_intro_2"]
    count = 1
    for doi, articles in duplicates.items():
        dup_case = str(count) + ") " + LANG[lang]["dup_case"].format(articles[0][3])
        institutions = []
        for article in articles:
            institution = article[0]
            for line in ins_content:
                if line[0] == institution:
                    pair = "* " + institution + " (" + line[2] + ")"
                    institutions.append(pair)
        dup_case += "\n".join(institutions) + "\n\n"
        markdown += dup_case
        markdown += LANG[lang]["dup_th"]
        for article in articles:
            row = "|"
            for index in [0, 1, 2, 6]:
                row += article[index] + "|"
            markdown += row + "\n"
        markdown += "\n"
        count += 1
    return markdown

def generate_apc_deviaton_section(institution, articles, stats, lang):
    md_content = ""
    journal_dict = {}
    for article in articles:
        journal = article[6]
        if journal not in journal_dict:
            journal_dict[journal] = [article]
        else:
            journal_dict[journal].append(article)
    journals = list(journal_dict.keys())
    journals.sort()
    md_content += LANG[lang]["ad_header"]
    md_content += LANG[lang]["ad_intro"]
    md_content += LANG[lang]["ad_disc"]
    for journal in journals:
        publisher = journal_dict[journal][0][5]
        num_articles = journal_dict[journal][0][21]
        md_content += LANG[lang]["ad_table_header"].format(journal, publisher, num_articles)
        md_content += LANG[lang]["ad_th"]
        for article in journal_dict[journal]:
            row = "|"
            for index in [1, 3, 2, 18, 19, 20]:
                elem = str(article[index]).replace("|", "\|")
                if index == 3: # doi
                    elem = "[" + elem + "](https://doi.org/" + elem + ")"
                if index in [2, 18, 19, 20]: # monetary
                    elem = elem + "€"
                row += elem + "|"
            row += "\n"
            md_content += row
        md_content += "\n\n"
    md_content += LANG[lang]["ad_stats_header"].format(institution)
    for stat in ["articles", "not_checked", "within_limits", "significant"]:
        md_content += "* " + LANG[lang]["ad_stats_" + stat]
        md_content += ": " + str(stats[stat]) + "\n"
    return md_content

def find_significant_apc_differences(apc_content, institution, verbose=False):
    titles = {}
    articles = []
    # 1st run: Find all journals the institution has published articles in
    for line in apc_content:
        if line[0] != institution or not oat.has_value(line[3]):
            continue
        title = line[6]
        if title not in titles:
            titles[title] = {"lines": []}
        articles.append(line)
    # 2nd run: Aggregate all articles for the journals found in 1
    for line in apc_content:
        title = line[6]
        if title in titles:
            titles[title]["lines"].append(line)
    for title in titles:
        apc_values = [float(line[2]) for line in titles[title]["lines"]]
        titles[title]["count"] = len(apc_values)
        titles[title]["stddev"] = stddev(apc_values)
        titles[title]["mean"] = mean(apc_values)

    stats = {
        "articles": len(articles),
        "not_checked": 0,
        "within_limits": 0,
        "significant": 0
    }
    sig_articles = []
    for article in articles:
        apc = article[2]
        doi = article[3]
        title = article[6]
        if titles[title]["count"] < 20:
            if verbose:
                msg = 'Article {}, journal "{}": Could not check costs, too few occurences ({})'
                oat.print_b(msg.format(doi, title, titles[title]["count"]))
            stats["not_checked"] += 1
            continue
        if abs(float(apc) - titles[title]["mean"]) > 2 * titles[title]["stddev"]:
            rounded_mean = round(titles[title]["mean"], 2)
            rounded_stddev = round(titles[title]["stddev"], 2)
            diff = round(float(apc) - rounded_mean, 2)
            if verbose:
                msg = ('Article {}, journal "{}": Cost ({}€) differs more than 2 standard ' +
                       'deviations (2 * {}€) from mean APC ({}€)')
                oat.print_y(msg.format(doi, title, apc, rounded_stddev, rounded_mean))
            stats["significant"] += 1
            article.append(rounded_mean)
            article.append(rounded_stddev)
            article.append(diff)
            article.append(titles[title]["count"])
            sig_articles.append(article)
        else:
            if verbose:
                msg = ('Article {}, journal "{}": No significant cost difference ({}€, mean ' +
                       'APC is {}€)')
                oat.print_g(msg.format(doi, title, apc, round(titles[title]["mean"], 2)))
            stats["within_limits"] += 1
    if verbose:
        oat.print_g("\nAnalysis finished, results:")
        for key, value in stats.items():
            oat.print_g(key + ": " + str(value))
    return sig_articles, stats

def main():
    args = parse()
    _, apc_content = oat.get_csv_file_content("../data/apc_de.csv", "utf-8", True)
    _, ins_content = oat.get_csv_file_content("../data/institutions.csv", "utf-8", True)
    _, dup_content = oat.get_csv_file_content("../data/unresolved_duplicates.csv", "utf-8", True)

    sig_articles, stats = find_significant_apc_differences(apc_content, args.institution,
                                                           args.verbose)

    report = ""
    report += generate_header(args.lang)
    report += generate_metadata_section(args.institution, ins_content, stats, args.lang)
    report += generate_duplicates_section(args.institution, dup_content, ins_content, args.lang)
    report += generate_apc_deviaton_section(args.institution, sig_articles, stats, args.lang)

    ins = args.institution.lower().replace(" ", "_")
    today = format_date(date.today(), format="dd_MM_yy")
    file_name = "report_" + ins + "_" + today + ".pdf"
    with open("report.md", "w") as out:
        out.write(report)
    run(["pandoc", "report.md", "-f", "markdown", "-o", file_name, "--pdf-engine=xelatex"])


if __name__ == '__main__':
    main()
