# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework import permissions
from .models import proteins, domainAssignment, domains
from .serializers import proteinsSerializer, domainAssignmentSerializer, domainsSerializer
from .forms import ProteinsForm


class proteinsApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        form = ProteinsForm(request.data)
        if form.is_valid():
            form.save()
            return Response({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class proteinInfoView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, protein_id, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        # get both the protein and domain assignment objects and serialize results
        proteinObj = proteins.objects.get(proteinID=protein_id)
        domainAssignmentObj = domainAssignment.objects.filter(
            protein=proteinObj)
        # domainAssignmentObjList = domainAssignment.objects.filter(protein=proteinObj)

        serializerProteins = proteinsSerializer(proteinObj)
        serializerDomainAssignment = domainAssignmentSerializer(
            domainAssignmentObj, many=True)
        # serializerDomainAssignmentList = domainAssignmentSerializer(
        #    domainAssignmentObj)
        # create result object by combining data from all 3 models

        taxonomyObj = {}
        length = 0
        # Restructing the results for the required output
        if not domainAssignmentObj:
            taxonomyObj = {}
        else:
            length = serializerDomainAssignment.data[0]['lengthProtein']
            names = serializerDomainAssignment.data[0]['organismScientificName'].split(
            )
            taxonomyObj = {
                'taxa_id': serializerDomainAssignment.data[0]['organismTaxaID'], 'clade': serializerDomainAssignment.data[0]['organismCladeIdenitifer'],
                'genus': names[0], 'species': names[1]}

        domainAssignmentObjects = []
        list = serializerDomainAssignment.data

        for thisDomainAssignment in list:
            domainDesc = thisDomainAssignment['domainDescription']
            domain = domains.objects.get(
                domainID=thisDomainAssignment['domainID'])
            domainSerializer = domainsSerializer(domain)
            # domainDesc.replace(" ", "")
            pfamObj = {'domain_id': thisDomainAssignment['domainID'],
                       'domain_description': domainSerializer.data['pfamFamilyDescription']}
            domainObj = {'pfam_id': pfamObj, 'description': domainDesc,
                         'start': thisDomainAssignment['domainStart'], 'stop': thisDomainAssignment['domainEndCoordinate']}
            domainAssignmentObjects.append(domainObj)

        newdict = {
            'proteinID': serializerProteins.data['proteinID'], 'sequence': serializerProteins.data['sequence'], 'taxonomy': taxonomyObj,
            'length': length, 'domains': domainAssignmentObjects}

        return Response(newdict, status=status.HTTP_200_OK)

# GET  http://127.0.0.1:8000/api/pfam/[PFAM ID] - return the domain and it's deacription


class DomainDetailView(APIView):
    def get(self, request, pfam_id, *args, **kwargs):
        try:

            domain = domains.objects.get(domainID=pfam_id)
            serializer = domainsSerializer(domain)
            response_data = {
                'domain_id': serializer.data['domainID'],
                'domain_description': serializer.data['pfamFamilyDescription'],
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except domains.DoesNotExist:
            return Response({'error': 'Domain not found'}, status=status.HTTP_404_NOT_FOUND)

# GET  http://127.0.0.1:8000/api/proteins/[TAXA ID] - return a list of all proteins for a given organism


class OrganismProteinsView(APIView):
    def get(self, request, taxa_id, *args, **kwargs):
        try:

            domainAssignmentObj = domainAssignment.objects.filter(
                organismTaxaID=taxa_id)
            serializerDomainAssignment = domainAssignmentSerializer(
                domainAssignmentObj, many=True)

            domainObjects = []
            list = serializerDomainAssignment.data

            for domain in list:
                domainObj = {'id': domain['id'],
                             'protein_id': domain['protein']}
                domainObjects.append(domainObj)

            return Response(domainObjects, status=status.HTTP_200_OK)
        except domains.DoesNotExist:
            return Response({'error': 'Domain not found'}, status=status.HTTP_404_NOT_FOUND)


class OrganismDomainsView(APIView):
    def get(self, request, taxa_id, *args, **kwargs):
        try:
            domainAssignmentObj = domainAssignment.objects.filter(
                organismTaxaID=taxa_id)

            serializerDomainAssignment = domainAssignmentSerializer(
                domainAssignmentObj, many=True)

            domainAssignmentObjects = []
            list = serializerDomainAssignment.data

            for thisDomainAssignment in list:
                domainDesc = thisDomainAssignment['domainDescription']
                domain = domains.objects.get(
                    domainID=thisDomainAssignment['domainID'])
                domainSerializer = domainsSerializer(domain)

                pfamObj = {'domain_id': thisDomainAssignment['domainID'],
                           'domain_description': domainSerializer.data['pfamFamilyDescription']}
                domainObj = {
                    'id': thisDomainAssignment['id'], 'pfam_id': pfamObj}
                domainAssignmentObjects.append(domainObj)

            return Response(domainAssignmentObjects, status=status.HTTP_200_OK)
        except domains.DoesNotExist:
            return Response({'error': 'Domain not found'}, status=status.HTTP_404_NOT_FOUND)


class ProteinCoverageView(APIView):
    def get(self, request, protein_id, *args, **kwargs):
        try:
            proteinObj = proteins.objects.get(proteinID=protein_id)
            domainAssignmentObj = domainAssignment.objects.filter(
                protein=proteinObj)
        # domainAssignmentObjList = domainAssignment.objects.filter(protein=proteinObj)

            serializerDomainAssignment = domainAssignmentSerializer(
                domainAssignmentObj, many=True)

            return Response(serializerDomainAssignment.data, status=status.HTTP_200_OK)
        except domains.DoesNotExist:
            return Response({'error': 'Domain not found'}, status=status.HTTP_404_NOT_FOUND)
