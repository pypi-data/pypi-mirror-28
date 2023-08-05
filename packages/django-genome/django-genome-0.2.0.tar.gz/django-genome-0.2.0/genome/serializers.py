# -*- coding: utf-8 -*-
from genomix.fields import DisplayChoiceField
from rest_framework import serializers

from . import choices, models


class GeneSerializer(serializers.ModelSerializer):
    """Serializer for Genes."""

    status = DisplayChoiceField(choices=choices.HGNC_GENE_STATUS)
    chromosome = serializers.StringRelatedField()
    synonyms = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Gene
        fields = (
            'id', 'hgnc_id', 'symbol', 'name', 'status', 'chromosome', 'synonyms',
            'active', 'created', 'modified',
        )


class TranscriptSerializer(serializers.ModelSerializer):
    """Serializer for Transcripts."""

    gene = serializers.StringRelatedField()
    strand = DisplayChoiceField(choices=choices.STRAND_TYPES)

    class Meta:
        model = models.Transcript
        fields = (
            'id', 'label', 'gene', 'strand',
            'transcription_start', 'transcription_end', 'cds_start', 'cds_end',
            'active', 'created', 'modified',
        )


class ExonSerializer(serializers.ModelSerializer):
    """Serializer for Exons."""

    transcript = serializers.StringRelatedField()

    class Meta:
        model = models.Exon
        fields = (
            'id', 'number', 'transcript',
            'start', 'end', 'cds',
            'active', 'created', 'modified',
        )
