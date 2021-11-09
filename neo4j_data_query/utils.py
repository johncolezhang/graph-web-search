import re
from collections import defaultdict
import pandas as pd

def position_map_util(NC_change_code):
    find_list = re.findall(r"chromosome [\dX]+", NC_change_code)
    if len(find_list) > 0:
        chr_name = find_list[0].replace("chromosome ", "chr")
        position_list = [
            "{}:{}".format(
                chr_name,
                "".join(["{}:{}".format(x.strip().replace("g.", "").replace(y, ""), y)
                         for y in
                         re.findall(r"[\D]+", x.strip().replace("g.", ""))]) if "del" not in x else x.strip().replace(
                    "g.", "")
            )
            for x in NC_change_code.split(";")[1].strip().replace("[", "").replace("]", "").replace("'", "").split(",")
        ]
        return position_list

    else:
        return []


def generate_mapping_csv():
    from py2neo import Graph
    import pandas as pd
    session = Graph("neo4j://172.16.229.46:7687", auth=("neo4j", "123456"))
    query_str = """
    match (hap:haplotype) 
    return hap.variant_name as variant_name, hap.NC_change_code as NC_change_code, 
    hap.mapped_rsID as mapped_rsID
    """
    result_list = session.run(query_str).data()
    df_mapping = pd.DataFrame(result_list)
    df_mapping = df_mapping[(df_mapping["NC_change_code"] != "") & (df_mapping["mapped_rsID"] != "")]
    df_mapping = df_mapping.sort_values(by=["variant_name"])
    position_list = [",".join(position_map_util(x)) for x in df_mapping["NC_change_code"].values]
    df_mapping = df_mapping.assign(position=position_list)
    rsID_list = [",".join(list(filter(lambda x: x != "", [x.strip() for x in x.split(",")]))) for x in
                 df_mapping["mapped_rsID"].values]
    df_mapping = df_mapping.assign(rsID=rsID_list)
    df_mapping = df_mapping[["variant_name", "position", "rsID"]]
    df_mapping.to_csv("neo4j_data_query/position_map.csv", index=False)

    query_str = """
    match (rs:rsID)
    return rs.variant_name as rsID, rs.position as position
    """
    result_list = session.run(query_str).data()
    df_mapping = pd.DataFrame(result_list).fillna("")
    df_mapping = df_mapping[df_mapping["position"] != ""]
    df_mapping.to_csv("neo4j_data_query/rsID_position_map.csv", index=False)


class Mapping:
    def __init__(self):
        df_mapping = pd.read_csv("neo4j_data_query/position_map.csv").fillna("")
        self.rsID_reverse_dict = defaultdict(list)
        self.rsID_dict = defaultdict(list)
        self.position_reverse_dict = defaultdict(list)
        self.position_dict = defaultdict(list)
        self.rsID_pos_dict = defaultdict(list)
        self.pos_rsID_dict = {}

        for index, row in df_mapping.iterrows():
            rs_list = row["rsID"].split(",")
            for rs in rs_list:
                self.rsID_reverse_dict[row["variant_name"]].append(rs)
                self.rsID_dict[rs].append(row["variant_name"])
            pos_list = row["position"].split(",")
            for pos in pos_list:
                self.position_reverse_dict[row["variant_name"]].append(pos)
                self.position_dict[pos].append(row["variant_name"])

        df_rs_mapping = pd.read_csv("neo4j_data_query/rsID_position_map.csv").fillna("")

        for index, row in df_rs_mapping.iterrows():
            for pos in row["position"].split(","):
                self.rsID_pos_dict[row["rsID"]].append(pos)
                self.pos_rsID_dict[pos] = row["rsID"]


    def rsID_to_haplotype(self, rsID_list):
        result_list = []
        rsID_list = list(filter(lambda x: x in self.rsID_dict.keys(), rsID_list))
        rs_sub_dict = defaultdict(list)

        for rsID in rsID_list:
            rs_sub_dict[rsID].extend(self.rsID_dict[rsID])

        rs_sub_dict = {x: list(set(y)) for x, y in rs_sub_dict.items()}
        candidate_haplotype_list = []
        sub_haplotype_dict = defaultdict(list)

        for x, y in rs_sub_dict.items():
            candidate_haplotype_list.extend(y)
            for i in y:
                sub_haplotype_dict[i].append(x)

        candidate_haplotype_list = list(set(candidate_haplotype_list))

        candidate_dict = {x: self.rsID_reverse_dict[x] for x in candidate_haplotype_list}
        sub_haplotype_dict = {x: list(set(y)) for x, y in sub_haplotype_dict.items()}

        for key in candidate_dict.keys():
            candidate_sort = ",".join(sorted(list(candidate_dict[key])))
            sub_sort = ",".join(sorted(list(sub_haplotype_dict[key])))
            if candidate_sort == sub_sort:
                result_list.append({"haplotype": key, "rsID": candidate_dict[key]})

        return result_list


    def position_to_haplotype(self, position_list):
        result_list = []
        position_list = list(filter(lambda x: x in self.position_dict.keys(), position_list))
        pos_sub_dict = defaultdict(list)

        for pos in position_list:
            pos_sub_dict[pos].extend(self.position_dict[pos])

        pos_sub_dict = {x: list(set(y)) for x, y in pos_sub_dict.items()}
        candidate_haplotype_list = []
        sub_haplotype_dict = defaultdict(list)

        for x, y in pos_sub_dict.items():
            candidate_haplotype_list.extend(y)
            for i in y:
                sub_haplotype_dict[i].append(x)

        candidate_haplotype_list = list(set(candidate_haplotype_list))

        candidate_dict = {x: self.position_reverse_dict[x] for x in candidate_haplotype_list}
        sub_haplotype_dict = {x: list(set(y)) for x, y in sub_haplotype_dict.items()}

        for key in candidate_dict.keys():
            candidate_sort = ",".join(sorted(list(candidate_dict[key])))
            sub_sort = ",".join(sorted(list(sub_haplotype_dict[key])))
            if candidate_sort == sub_sort:
                result_list.append({"haplotype": key, "position": candidate_dict[key]})

        return result_list


    def rsID_to_position(self, rsID_list):
        result_dict = {}
        for rsID in rsID_list:
            result_dict[rsID] = self.rsID_pos_dict.get(rsID, [])
        return [{"rsID": key, "position": value} for key, value in result_dict.items()]


    def position_to_rsID(self, position_list):
        result_dict = {}
        for pos in position_list:
            result_dict[pos] = self.pos_rsID_dict.get(pos, "")

        return [{"position": key, "rsID": value} for key, value in result_dict.items()]


if __name__ == "__main__":
    generate_mapping_csv()
    # mapping = Mapping()
    # test_list = [
    #     ['chr7:117614699:G>C', 'chr7:117606695:C>T'],
    #     ['chr19:41010088:C>G', 'chr19:41012465:C>T'],
    #     ['chr22:42130710:G>A', 'chr22:42130692:G>A', 'chr22:42129130:C>G', 'chr22:42126611:C>G'],
    #     ['chr22:42130692:G>A', 'chr22:42129130:C>G', 'chr22:42128848:C>T', 'chr22:42126611:C>G']
    # ]
    # for tl in test_list:
    #     result = mapping.position_to_haplotype(tl)
    #     print(result)
