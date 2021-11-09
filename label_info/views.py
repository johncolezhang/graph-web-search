from django.http import HttpResponse
import json
from query_utils.db_util import DbUtil

def add_label_info(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        label_tile = request.POST['label_tile']
        label_sub_title = request.POST['label_sub_title']
        label_content = request.POST['label_content']
    except Exception as e:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))


    insert_dict = {
        "label_tile": label_tile,
        "label_sub_title": label_sub_title,
        "label_content": label_content
    }

    try:
        db_util = DbUtil()
        db_util.insert_data(table_name="labels", data_list=[insert_dict])
    except Exception as e:
        return HttpResponse(json.dumps({"success": False, "message": str(e)}, indent=4))

    return HttpResponse(json.dumps({"success": True, "message": "插入成功"}, indent=4))


def get_label_info(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": False, "message": "请使用post调用接口"}, indent=4))

    try:
        label_tile = request.POST['label_tile']
    except Exception as e:
        return HttpResponse(json.dumps({"success": False, "message": "请检查参数输入"}, indent=4))

    try:
        db_util = DbUtil()
        result_list = db_util.select_table(
            table_name="labels",
            filter_dict={"label_title": label_tile},
            field_list=["label_tile", "label_sub_title", "label_content"]
        )
    except Exception as e:
        return HttpResponse(json.dumps({"success": False, "message": str(e)}, indent=4))

    response_dict = {"success": True, "result": result_list}
    return HttpResponse(json.dumps(response_dict, indent=4))
