from rest_framework import serializers
from .models import proteins, domainAssignment, domains


class proteinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = proteins
        fields = ["proteinID", "sequence"]


class domainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = domains
        fields = ["domainID", "pfamFamilyDescription"]


class domainAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = domainAssignment
        fields = ["protein", "organismTaxaID", "organismCladeIdenitifer", "organismScientificName",
                  "domainDescription", "domainID", "domainStart", "domainEndCoordinate", "lengthProtein", "id"]


class domainAssignmentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = domainAssignment
        fields = ["domainDescription", "domainID", "domainStart",
                  "domainEndCoordinate", "lengthProtein"]
