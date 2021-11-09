from django.http import HttpResponse
from django.shortcuts import render
import json
from query_utils.neo4j_util import neo4jUtil
from neo4j_data_query.utils import position_map_util, Mapping
import re

pos_mapping = Mapping()

def variant_mapping_page(request):
    return render(request, "variant_mapping.html")

def variant_info_page(request):
    return render(request, "variant_info.html")

def get_genes(request):
    """
    获取所有基因list
    :param request:
    :return:
    """
    n_util = neo4jUtil()
    query_template = """
        match (n:gene)
        return n.gene_name as gene_name
    """
    result = n_util.run_cypher(query_template)

    response_dict = {"success": True, "result": result}
    return HttpResponse(json.dumps(response_dict, indent=4))


def get_gene_genotypes(request):
    """
    输入基因名，获取该基因的基因型list
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        gene_name = request.POST['gene_name']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    n_util = neo4jUtil()
    query_template = """
    match (n:gene {{gene_name: "{}"}})<-[r:mutation_at]-(m:haplotype)
    return m.variant_name as variant_name
    """.format(gene_name)

    result = n_util.run_cypher(query_template)
    result = list(sorted(map(lambda x: x["variant_name"], result)))

    response_dict = {"success": True, "gene_name": gene_name, "genotypes": result}
    return HttpResponse(json.dumps(response_dict, indent=4))


def get_nmpa_drugs(request):
    """
    输入药名，获取包含该药的nmpa上市药list
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        drug_name = request.POST['drug_name']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    n_util = neo4jUtil()
    query_template = """
    match (n:drug {{display: "{}"}})-[]-(che:chemical)-[]-(nm:nmpa_drug)
    return nm.drug_name_chn as drug_name_chn, nm.drug_name_eng as drug_name_eng, 
    nm.drug_code as drug_code, nm.license as license, 
    nm.chn_business_name as chn_business_name, nm.eng_business_name as eng_business_name,
    nm.country as country, nm.company as company 
    order by drug_name_chn
    """.format(drug_name)
    result = n_util.run_cypher(query_template)

    response_dict = {"success": True, "drug_name": drug_name, "nmpa_drugs": result}
    return HttpResponse(json.dumps(response_dict, indent=4))


def get_ATC_info(request):
    """
    输入ATC代码，获取ATC代码详情
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        ATC_code = request.POST['ATC_code']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    response_dict = {"success": True, "ATC_code": ATC_code}
    return HttpResponse(json.dumps(response_dict, indent=4))


def get_diplotype_info(request):
    """
    输入双体型，获取双体型详情
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        diplotype_name = request.POST['diplotype_name']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    # 需要获取药物详情，医保标签，FDA黑框标签
    n_util = neo4jUtil()
    query_template = """
    MATCH (n:diplotype {{display: "{}"}}) RETURN properties(n) as properties
    """.format(diplotype_name)

    result = n_util.run_cypher(query_template)

    if len(result) > 0:
        result = result[0]["properties"]
        frequency_dict = json.loads(result.get("frequency", "{}").replace("'", "\""))
        frequency_list = []
        for key, value in frequency_dict.items():
            if key != "update_date":
                frequency_list.append({"area": key, "frequency": value})
        frequency_dict = {"bio_geo": frequency_list, "update_date": frequency_dict.get("update_date", "")}
        result["frequency"] = frequency_dict
    else:
        result = dict()

    response_dict = {"success": True, "diplotype_name": diplotype_name, "result": result}
    return HttpResponse(json.dumps(response_dict, indent=4))


def get_haplotype_info(request):
    """
    输入单体型，获取双体型详情
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        haplotype_name = request.POST['haplotype_name']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    n_util = neo4jUtil()
    query_template = """
    MATCH (n:haplotype {{display: "{}"}}) RETURN properties(n) as properties
    """.format(haplotype_name)

    result = n_util.run_cypher(query_template)

    if len(result) > 0:
        result = result[0]["properties"]
        frequency_dict = json.loads(result.get("frequency", "{}").replace("'", "\""))
        frequency_list = []
        for key, value in frequency_dict.items():
            if key != "update_date":
                frequency_list.append({"area": key, "frequency": value})
        frequency_dict = {"bio_geo": frequency_list, "update_date": frequency_dict.get("update_date", "")}
        result["frequency"] = frequency_dict

        functionality_dict = json.loads(result.get("functionality", "{}").replace("'", "\""))
        functionality_list = []
        for key, value in functionality_dict.items():
            if key != "update_date":
                functionality_list.append({"name": key, "detail": value})
        functionality_dict = {"functionality": functionality_list, "update_date": functionality_dict.get("update_date", "")}
        result["functionality"] = functionality_dict
    else:
        result = dict()

    response_dict = {"success": True, "haplotype_name": haplotype_name, "result": result}
    return HttpResponse(json.dumps(response_dict, indent=4))


def get_drug_info(request):
    """
    输入药名，获取药物详情
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        drug_name = request.POST['drug_name']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    # 需要获取药物详情，医保标签，FDA黑框标签
    n_util = neo4jUtil()
    query_template = """
    match (n:drug {{display: "{}"}})
    return n.drug_name as drug_name, n.indication as indication,
    n.component as component, n.in_medical_insurance as in_medical_insurance,
    n.insurance_level as insurance_level, n.insurance_dosage_form as insurance_dosage_form,
    n.insurance_drug_category as insurance_drug_category,
    n.has_fda_warning as has_fda_warning
    """.format(drug_name)
    result = n_util.run_cypher(query_template)

    if len(result) > 0:
        result = result[0]
    else:
        result = dict()

    response_dict = {"success": True, "drug_name": drug_name}
    for key, value in result.items():
        response_dict[key] = value

        if key in ["in_medical_insurance", "has_fda_warning"]:
            if value and value == "是":
                response_dict[key] = True
            else:
                response_dict[key] = False

    return HttpResponse(json.dumps(response_dict, indent=4))


def get_guideline_info(request):
    """
    输入药名及双体型，获取药物指南数据
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        drug_name = request.POST['drug_name']
        diplotype_name = request.POST['diplotype_name']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    n_util = neo4jUtil()
    query_template = """
    match p = (d:drug {{display: "{}"}})
    <-[r1:chemical_drug_relation]-(che:chemical)
    <-[r2]-(dip:diplotype {{display: "{}"}})
    return d.drug_name as drug_name,
    che.chemical_name as chemical_name,
    properties(r2) as relation_properties,
    dip.diplotype_name as diplotype_name
    """.format(drug_name, diplotype_name)
    result = n_util.run_cypher(query_template)

    response_dict = {"success": True, "drug_name": drug_name,
                     "diplotype_name": diplotype_name, "relations": result}
    return HttpResponse(json.dumps(response_dict, indent=4))


def get_similar_drugs(request):
    """
    输入药名，获取相似药品名
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        drug_name = request.POST['drug_name']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    response_dict = {"success": True, "drug_name": drug_name}
    return HttpResponse(json.dumps(response_dict, indent=4))


def is_pgx_drug(request):
    """
    输入药名，返回是否是pgx药物
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        drug_name = request.POST['drug_name']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    n_util = neo4jUtil()
    # 获取pgx标签
    query_template = """
    match (n:drug {{drug_name: "{drug_name}"}})<-[:chemical_drug_relation]-(m:chemical)<-[]-(v:variant)
    return n.drug_name as drug_name
    union
    match (n:drug {{drug_name: "{drug_name}"}})<-[:chemical_drug_relation]-(m:chemical)<-[]-(dip:diplotype)
    return n.drug_name as drug_name
    union
    match (n:drug {{drug_name: "{drug_name}"}})<-[:chemical_drug_relation]-(m:chemical)<-[]-(ge:gene)
    return n.drug_name as drug_name
    """.format(drug_name=drug_name)
    result = n_util.run_cypher(query_template)

    if len(result) > 0:
        is_pgx = True
    else:
        is_pgx = False

    response_dict = {"success": True, "drug_name": drug_name, "is_pgx": is_pgx}
    return HttpResponse(json.dumps(response_dict, indent=4))


def from_haplotype_to_position_and_rsID(request):
    """
    输入基因型，返回基因型坐标
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        haplotype_name = request.POST['haplotype_name']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    n_util = neo4jUtil()
    query_template = """
    match (n:haplotype {{display:"{}"}}) 
    return n.NC_change_code as NC_change_code, n.is_reference as is_reference,
    n.mapped_rsID as mapped_rsID, n.variant_name as variant_name
    """.format(haplotype_name)

    result = n_util.run_cypher(query_template)
    if len(result) != 0:
        NC_change_code = result[0]["NC_change_code"]
        position_list = position_map_util(NC_change_code)

        is_reference = result[0]["is_reference"]
        is_reference = True if is_reference and is_reference == "True" else False

        mapped_rsID = list(filter(lambda x: x!= "", [x.strip() for x in result[0]["mapped_rsID"].split(",")]))
        result = {
            "position_list": position_list,
            "is_reference": is_reference,
            "rsID_list": mapped_rsID
        }

    response_dict = {"success": True, "haplotype_name": haplotype_name, "result": result}
    return HttpResponse(json.dumps(response_dict, indent=4))


def from_position_to_haplotype(request):
    """
    输入坐标，返回基因型
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        position = request.POST['position']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    position_list = list(filter(lambda x: x.strip() != "", re.split("[ |;|,|\n]", position)))

    result = pos_mapping.position_to_haplotype(position_list=position_list)
    response_dict = {"success": True, "position": position_list, "result": result}
    return HttpResponse(json.dumps(response_dict, indent=4))


def from_position_to_rsID(request):
    """
    输入坐标，返回rsID
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        position = request.POST['position']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    position_list = list(filter(lambda x: x.strip() != "", re.split("[ |;|,|\n]", position)))

    result = pos_mapping.position_to_rsID(position_list=position_list)
    response_dict = {"success": True, "position": position_list, "result": result}
    return HttpResponse(json.dumps(response_dict, indent=4))


def from_rsID_to_position(request):
    """
    输入坐标，返回rsID
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        rsID = request.POST['rsID']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    rsID_list = list(filter(lambda x: x.strip() != "", re.split("[ |;|,|\n]", rsID)))
    result = pos_mapping.rsID_to_position(rsID_list=rsID_list)
    response_dict = {"success": True, "rsID": rsID_list, "result": result}
    return HttpResponse(json.dumps(response_dict, indent=4))


def from_rsID_to_haplotype(request):
    """
    输入rsID，返回基因型
    :param request:
    :return:
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        rsID = request.POST['rsID']
    except:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    rsID_list = list(filter(lambda x: x.strip() != "", re.split("[ |;|,|\n]", rsID)))
    result = pos_mapping.rsID_to_haplotype(rsID_list=rsID_list)
    response_dict = {"success": True, "rsID": rsID_list, "result": result}
    return HttpResponse(json.dumps(response_dict, indent=4))

