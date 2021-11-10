from django.urls import path
from . import views

urlpatterns = [
    path("", views.variant_mapping_page),
    path("variant_mapping_page", views.variant_mapping_page),
    path("variant_info_page", views.variant_info_page),
    path("variant_drug_page", views.variant_drug_page),

    path("get_nmpa_drugs", views.get_nmpa_drugs), # for search
    path("get_ATC_info", views.get_ATC_info), # for search
    path("get_similar_drugs", views.get_similar_drugs),  # for search
    path("is_pgx_drug", views.is_pgx_drug),  # for search
    path("get_drug_info", views.get_drug_info),  # for search

    path("get_genes", views.get_genes), # for kb
    path("get_gene_genotypes", views.get_gene_genotypes), # for kb
    path("get_diplotype_info", views.get_diplotype_info), # for kb
    path("get_haplotype_info", views.get_haplotype_info), # for kb
    path("get_guideline_info", views.get_guideline_info),
    path("from_haplotype_to_position_and_rsID", views.from_haplotype_to_position_and_rsID), # for kb
    path("from_position_to_haplotype", views.from_position_to_haplotype), # for kb
    path("from_position_to_rsID", views.from_position_to_rsID), # for kb
    path("from_rsID_to_position", views.from_rsID_to_position), # for kb
    path("from_rsID_to_haplotype", views.from_rsID_to_haplotype), # for kb
    path("get_rsID_chemical_relation", views.get_rsID_chemical_relation), # for kb
    path("get_gene_chemical_relation", views.get_gene_chemical_relation), # for kb
    path("get_haplotype_chemical_relation", views.get_haplotype_chemical_relation), # for kb
    path("get_diplotype_chemical_relation", views.get_diplotype_chemical_relation), # for kb
]

