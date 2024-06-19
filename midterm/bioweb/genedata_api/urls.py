from django.urls import path
from .views import (proteinsApiView, proteinInfoView,
                    DomainDetailView, OrganismProteinsView, OrganismDomainsView, ProteinCoverageView)

urlpatterns = [
    path('protein/', proteinsApiView.as_view(), name='proteins-api'),
    path('protein/<str:protein_id>',
         proteinInfoView.as_view(), name='protein-info'),
    path('pfam/<str:pfam_id>/', DomainDetailView.as_view(), name='domain-detail'),
    path('proteins/<str:taxa_id>/', OrganismProteinsView.as_view(),
         name='organism-proteins-detail'),
    path('pfams/<str:taxa_id>/', OrganismDomainsView.as_view(),
         name='organism-domains'),
]
