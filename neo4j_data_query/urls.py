from django.urls import path
from . import views


urlpatterns = [
    path("", views.variant_mapping_page),
    path("variant_mapping_page", views.variant_mapping_page),
    path("variant_info_page", views.variant_info_page),
    path("variant_drug_page", views.variant_drug_page),
    path("get_genes", views.get_genes),
    path("get_gene_genotypes", views.get_gene_genotypes),
    path("get_nmpa_drugs", views.get_nmpa_drugs),
    path("get_ATC_info", views.get_ATC_info),
    path("get_diplotype_info", views.get_diplotype_info),
    path("get_haplotype_info", views.get_haplotype_info),
    path("get_drug_info", views.get_drug_info),
    path("get_guideline_info", views.get_guideline_info),
    path("get_similar_drugs", views.get_similar_drugs),
    path("is_pgx_drug", views.is_pgx_drug),
    path("from_haplotype_to_position_and_rsID", views.from_haplotype_to_position_and_rsID),
    path("from_position_to_haplotype", views.from_position_to_haplotype),
    path("from_position_to_rsID", views.from_position_to_rsID),
    path("from_rsID_to_position", views.from_rsID_to_position),
    path("from_rsID_to_haplotype", views.from_rsID_to_haplotype),
    path("get_rsID_chemical_relation", views.get_rsID_chemical_relation),
    path("get_gene_chemical_relation", views.get_gene_chemical_relation),
    path("get_haplotype_chemical_relation", views.get_haplotype_chemical_relation),
    path("get_diplotype_chemical_relation", views.get_diplotype_chemical_relation),
]