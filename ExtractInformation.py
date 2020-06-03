import spacy
import neuralcoref
import os
from openie import StanfordOpenIE
import warnings
import random
from spacy.util import minibatch, compounding
from pathlib import Path

class ExtractInformation:
    IS_GPU = True
    SUBJECT = 'subject'
    SUBJECT_ENTITY = 'subject_entity'
    RELATION = 'relation'
    OBJECT = 'object'
    OBJECT_ENTITY = 'object_entity'

    ENTITY_NAME = 'name'
    ENTITY_TYPE = 'entity_type'

    ENTITY_SUBJECT_OTHER = 'subject_other'
    ENTITY_OBJECT_OTHER = 'object_other'

    def __init__(self, modelSpacy = 'en_core_web_lg', modelCoref = 'en'):
        print(os.path.dirname(spacy.__file__))
        if ExtractInformation.IS_GPU:
            spacy.prefer_gpu()

        self.modelSpacy = modelSpacy
        self.modelCoref = modelCoref
        self.stanfordClient = StanfordOpenIE()

        self.nlpCoref, self.nlpSpacy = self.initSpacy(modelSpacy, modelCoref)

    def initSpacy(self, modelSpacy, modelCoref):
        nlpSpacy = spacy.load(modelSpacy)

        nlpCoref = spacy.load('en')
        coref = neuralcoref.NeuralCoref(nlpCoref.vocab)
        nlpCoref.add_pipe(coref, name=modelCoref)

        return nlpCoref, nlpSpacy

    #Stage 1: replace Pronouns To Noun, example: My sister has a dog. She loves him. => Cluster: [My sister: [My sister, She], a dog: [a dog, him]]
    def replacePronounsToNoun(self, nlp, inputText):
        #todo unicode input Text
        #ouputText = unicode(inputText)
        ouputText = inputText
        doc = nlp(inputText)
        if (doc._.has_coref):
            ouputText = doc._.coref_resolved
        return doc._.has_coref, ouputText

    #Stage 2: Extract Entities
    def extractEntities(self, nlp, inputText):
        doc = nlp(inputText)
        entities = []
        for ent in doc.ents:
            entities.append({
                ExtractInformation.ENTITY_NAME : ent.text,
                ExtractInformation.ENTITY_TYPE : ent.label_
            })
        return entities

    #Stage 3: Extract Triple
    def extractTriple(self, inputText):
        hasCoref, inputText = self.replacePronounsToNoun(self.nlpCoref, inputText)

        #todo similaty relation
        tripleStanfords = self.extractTripleStanfordOpenIE(inputText)
        tripleSpacys = self.extractTripleSpacy(self.nlpSpacy, inputText)

        tripleTemps = tripleStanfords
        for tripleStanford in tripleStanfords:
            subject1 = tripleStanford.get(ExtractInformation.SUBJECT)
            relation1 = tripleStanford.get(ExtractInformation.RELATION)
            object1 = tripleStanford.get(ExtractInformation.OBJECT)
            for tripleSpacy in tripleSpacys:
                subject2 = tripleSpacy.get(ExtractInformation.SUBJECT)
                relation2 = tripleSpacy.get(ExtractInformation.RELATION)
                object2 = tripleSpacy.get(ExtractInformation.OBJECT)

                if ((subject1 == subject2)):
                    if ((object1 == object2) or (object1 in object2)):
                        text1 = self.nlpSpacy(relation1)
                        text2 = self.nlpSpacy(relation2)
                        if (text1.similarity(text2) > 0.6):
                            # tripleTemps.remove(tripleStanford)
                            break

        triples = tripleTemps + tripleSpacys

        for triple in triples:
            subjectEnts = self.nlpSpacy(triple.get(ExtractInformation.SUBJECT))
            triple[ExtractInformation.SUBJECT_ENTITY] = [(e.text, e.start_char, e.end_char, e.label_) for e in subjectEnts.ents]

            objectEnts = self.nlpSpacy(triple.get(ExtractInformation.OBJECT))
            triple[ExtractInformation.OBJECT_ENTITY] = [(e.text, e.start_char, e.end_char, e.label_) for e in objectEnts.ents]
        return triples

    def extractTripleStanfordOpenIE(self, inputText):
        triples = []
        try:
            triples = self.stanfordClient.annotate(inputText)
        except Exception as exception:
            print("--- extract Triple Stanford OpenIE Error " + str(exception))
        return triples

    def extractTripleSpacy(self, nlp, inputText):
        docSeparate = nlp(inputText)
        sentences = [sent.string.strip() for sent in docSeparate.sents]
        triples = []

        for sentence in sentences:
            doc = nlp(sentence)
            spans = list(doc.ents) + list(doc.noun_chunks)
            for span in spans:
                span.merge()

            for ent in doc.ents:
                preps = [prep for prep in ent.root.head.children if prep.dep_ == "prep"]
                for prep in preps:
                    for child in prep.children:
                        triples.append({
                            ExtractInformation.SUBJECT : ent.text,
                            ExtractInformation.RELATION : "{} {}".format(ent.root.head, prep),
                            ExtractInformation.OBJECT : child.text
                        })
        return triples

    def trainAdditionalEntity(self, train_data, label, nlp, model=None, n_iter=30):
        if ("ner" not in nlp.pipe_names):
            ner = nlp.create_pipe("ner")
            nlp.add_pipe(ner)
        else:
            ner = nlp.get_pipe("ner")
        ner.add_label(label)

        if model is None:
            optimizer = nlp.begin_training()
        else:
            optimizer = nlp.resume_training()

        # get names of other pipes to disable them during training
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

        # only train NER
        with nlp.disable_pipes(*other_pipes) and warnings.catch_warnings():
            # show warnings for misaligned entity spans once
            warnings.filterwarnings("once", category=UserWarning, module='spacy')

            sizes = compounding(1.0, 4.0, 1.001)
            # batch up the examples using spaCy's minibatch
            for itn in range(n_iter):
                random.shuffle(train_data)
                batches = minibatch(train_data, size=sizes)
                losses = {}
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
                print("Losses", losses)

        return nlp

    def saveModel(self, output_dir, nlp, new_model_name):
        if output_dir is not None:
            output_dir = Path(output_dir)
            if not output_dir.exists():
                output_dir.mkdir()
            nlp.meta["name"] = new_model_name  # rename model
            nlp.to_disk(output_dir)
            print("Saved model to", output_dir)

def dataCases():
    LABEL_CASE = "CASES"
    TRAIN_DATA_CASE = [
        (
            "there have been 6,140,934 confirmed cases",
            {"entities": [(26, 5, LABEL_CASE)]},
        ),
        (
            "Coronavirus Cases",
            {"entities": [(0, 17, LABEL_CASE)]},
        ),
        (
            "Active cases",
            {"entities": [(0, 12, LABEL_CASE)]},
        ),
        (
            "Closed cases",
            {"entities": [(0, 12, LABEL_CASE)]},
        ),
        (
            "Daily New Cases",
            {"entities": [(0, 15, LABEL_CASE)]},
        ),
        (
            "Total Cases",
            {"entities": [(0, 11, LABEL_CASE)]},
        ),
        (
            "New Cases",
            {"entities": [(0, 9, LABEL_CASE)]},
        ),
        (
            "Total Deaths",
            {"entities": [(0, 12, LABEL_CASE)]},
        ),
    ]

    return TRAIN_DATA_CASE, LABEL_CASE

def dataNCovi():
    LABEL_CASE = "Outbreak"
    TRAIN_DATA_CASE = [
        (
            "NCOVID-19",
            {"entities": [(0, 9, LABEL_CASE)]},
        ),
        (
            "Coronavirus disease",
            {"entities": [(0, 19, LABEL_CASE)]},
        ),
        (
            "COVID-19",
            {"entities": [(0, 8, LABEL_CASE)]},
        ),
        (
            "Disease",
            {"entities": [(0, 7, LABEL_CASE)]},
        ),
        (
            "Disease outbreaks",
            {"entities": [(0, 17, LABEL_CASE)]},
        ),
        (
            "Cholera",
            {"entities": [(0, 7, LABEL_CASE)]},
        )
    ]

    return TRAIN_DATA_CASE, LABEL_CASE

def trainModel():
    output_dir = 'model_dir'

    trainData, labelData = dataNCovi()
    extractInfo = ExtractInformation()
    nlp = extractInfo.trainAdditionalEntity(trainData, labelData, extractInfo.nlpSpacy)
    extractInfo.saveModel(output_dir, nlp, "modelNcovi")

def testModel():
    output_dir = 'en_core_web_lg'
    output_dir = 'model_dir'

    extractInfo = ExtractInformation(modelSpacy=output_dir)
    print(extractInfo.nlpSpacy.meta["name"])
    print(extractInfo.extractEntities(extractInfo.nlpSpacy, "My name is HaoLVb and Coronavirus Cases"))


if __name__ == '__main__':
    xinchao = 'xinchao'
    # text = "It's time to throw the school calendar out the window"
    # text = 'Barrack Obama was born in Hawaii in the year 1961. He was president of the United States.'

    # trainModel()
    # testModel()

    # print(ex.extractEntities(ex.nlpSpacy, text))
    # for item in ex.extractTriple(text):
    #     print(item)
