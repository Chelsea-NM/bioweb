from django.db import models


class proteins(models.Model):
    proteinID = models.CharField(primary_key=True, max_length=255)
    sequence = models.TextField(max_length=40000)

    def __str__(self):
        return self.proteinID


class domains(models.Model):
    domainID = models.CharField(primary_key=True, max_length=255)
    pfamFamilyDescription = models.CharField(max_length=255)

    def __str__(self):
        return self.domainID


class domainAssignment(models.Model):
    protein = models.ForeignKey(proteins, on_delete=models.CASCADE)
    organismTaxaID = models.CharField(max_length=255)
    organismCladeIdenitifer = models.CharField(max_length=255)
    organismScientificName = models.CharField(max_length=255)
    domainDescription = models.CharField(max_length=255)
    domainID = models.ForeignKey(domains, on_delete=models.CASCADE)
    domainStart = models.IntegerField()
    domainEndCoordinate = models.IntegerField()
    lengthProtein = models.IntegerField()

    def __str__(self):
        return self.protein.proteinID
