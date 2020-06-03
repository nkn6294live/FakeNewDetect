from sentence_transformers import SentenceTransformer
import scipy
from py2neo import Graph
import unidecode
from ExtractInformation import ExtractInformation

class GraphSearch:
    test = False

    entities_valid = [
        'Location', 'Case', '_T_Number', '_T_Date'
        'World', 'Country', 'City',
        'Admin1', 'Admin2',
        'UNIntermediateRegion', 'UNRegion', 'UNSubRegion', 'USRegion',
        'Clade', 'Variant', 'Genome', 'Organism', 'Outbreak', 'Strain',
        'Gene', 'Protein', 'Publication'
    ]

    relations_valid = [
        'IN', 'REPORTED_IN',
        "_P_CONFIRMED_PEOPLE", "_P_DEATH_PEOPLE", "_P_POPULATION", "_P_AREA_SQ_KM",
        'CARRIES', 'CAUSES' 'HAS'
                   "ENCODES", "HAS_VARIANT", "FOUND_IN", "MENTIONS", "RELATED_TO",
        "IS",
    ]

    entities_type_map = {
        # TODO update entities_type_map
        'PERSON': 'PERSON',
        'GPE': 'Location',
        'DATE': '_T_Date',
        'NUMBER': '_T_Number',
        'POPULATION': '_P_POPULATION',
        'AREA_SQ_KM': '_P_AREA_SQ_KM',
        'CONFIRMED_PEOPLE': '_P_CONFIRMED_PEOPLE',
        'DEATH_PEOPLE': '_P_DEATH_PEOPLE'
    }

    relations_type_map = {
        # TODO update relation_type_map
    }

    triples_valid = [
        # ("Admin1", "Country", "IN"),
        # ("Admin2", "Admin1", "IN"),
        # ("City", "Location", "IN"),
        # ("USRegion", "Country", "IN"),
        # ("USDivision", "USRegion", "IN"),
        # ("Admin1", "USDivision", "IN"),
        # ("UNRegion", "World", "IN"),
        # ("UNSubRegion", "UNRegion", "IN"),
        # ("UNIntermediateRegion", "UNSubRegion", "IN"),
        # ("Country", "UNRegion", "IN"),
        # ("Country", "UNRegion", "IN"),
        # ("Country", "UNSubRegion", "IN"),
        # ("Country", "UNIntermediateRegion", "IN"),
        ("Location", "Location", "IN"),

        # ("Country", "_T_Number", "_P_POPULATION"),#property
        # ("Country", "_T_Number", "_P_AREA_SQ_KM"),#property
        ("Location", "_T_Number", "_P_POPULATION"),  # property
        ("Location", "_T_Number", "_P_AREA_SQ_KM"),  # property

        # ("Cases", "_T_Number", "_T_Date", "_P_CONFIRMED_PEOPLE"),#property
        # ("Cases", "_T_Number", "_T_Date", "_P_DEATH_PEOPLE"),#property
        ("Location", "_T_Number", "_T_Date", "_P_CONFIRMED_PEOPLE"),  # property
        ("Location", "_T_Number", "_T_Date", "_P_DEATH_PEOPLE"),  # property
        # ("Cases", "Admin2", "_T_Date", "REPORTED_IN"),# need check
        ("Cases", "Location", "_T_Date", "REPORTED_IN"),  # need check

        # ("Strain", "Country", "FOUND_IN"),
        # ("Strain", "Admin1", "FOUND_IN"),
        # ("Strain", "Admin2", "FOUND_IN"),
        # ("Strain", "City", "FOUND_IN"),
        ("Strain", "Location", "FOUND_IN"),

        # ("Outbreak", "Cases", "RELATED_TO"),
        # ("Genome", "Strain", "IS"),
        # ("Organism", "Strain", "HAS"),
        # ("Organism", "Strain", "CARRIES"),
        # ("Strain", "Clade", "HAS"),
        # ("Genome", "Gene", "HAS"),
        # ("Gene", "Protein", "ENCODES"),

        # ("Strain", "Variant", "HAS_VARIANT"),
        # ("Gene", "Variant", "HAS_VARIANT"),
        # ("Publication", "Strain", "MENTIONS"),
        # ("Cases", "Outbreak", "RELATED_TO"),
        # ("Organism", "Outbreak", "CAUSES"),

        # ("Country", "Location", "IS"),
        # ("Admin1", "Location", "IS"),
        # ("Admin2", "Location", "IS"),
        # ("City", "Location", "IS"),
        # ("USRegion", "Location", "IS"),
        # ("USDivision", "Location", "IS"),
        # ("UNRegion", "Location", "IS"),
        # ("UNSubRegion", "Location", "IS"),
        # ("UNIntermediateRegion", "Location", "IS"),
        # ("World", "Location", "IS"),
    ]

    relation_type = [
        ("_P_CONFIRMED_PEOPLE", "property", "cummulativeConfirmed", "Cases"),
        ("_P_DEATH_PEOPLE", "property", "cummulativeDeaths", "Cases"),
        ("_P_POPULATION", "property", "population", 'Country'),
        ("_P_AREA_SQ_KM", "property", "areaSqKm", 'Country')
    ]

    alias_relation = ["IS", "EQ", "ALIAS"]
    def __init__(self, neo4j_host = "bolt://localhost:7687/", neo4j_user = "neo4j", neo4j_password = "neo4jbinder"):
       self.neo4j_host = neo4j_host
       self.neo4j_user = neo4j_user
       self.neo4j_password = neo4j_password
       self.model = SentenceTransformer('bert-base-nli-mean-tokens')
       # self.graph = Graph(self.neo4j_host, password=self.neo4j_password)
       self.graph = Graph(self.neo4j_host, user=self.neo4j_user, password=self.neo4j_password)
       self.extractInfo = ExtractInformation()

    def allIndexOf(self, value, list):
        results = []
        for index in range(len(list)):
            if value == list[index]: results.append(index)
        return results

    def check_entity_type(self, text):
        result = None
        if text in self.entities_type_map:
            text = self.entities_type_map[text]
        if (text in self.entities_valid): result = text
        return result

    def check_relation_type(self, type):
        result = None
        if type in self.relations_type_map:
            type = self.relations_type_map[type]
        if (type in self.relations_valid): result = type
        return result

    def normal_entity_value(self, value):
        # TODO normal entity value
        return value

    def normal_relation_value(self, value):
        # TODO normal entity value
        return value

    def extract_information(self, query):
        method_tag = "extract_information"
        # TODO mock extract_information data
        # entity21 = {'type': 'entity', 'label': 'Cases', 'value': 'Viet nam'}
        # entity22 = {'type': 'entity', 'label': '_T_Number', 'value': 100000}
        # entity23 = {'type': 'entity', 'label': 'Date', 'value': '20-01-2020'}
        # relation2 = {'type': 'relation', 'label': '_P_DEATH_PEOPLE', 'value': None}
        # entites = [
        #     # {'name': 'Barrack Obama', 'entity_type': 'PERSON'},
        #     # {'name': 'Hawaii', 'entity_type': 'GPE'},
        #     # {'name': 'the year 1961', 'entity_type': 'DATE'},
        #     # {'name': 'the United States', 'entity_type': 'GPE'}
        #     {'name': 'Hoang Sa', 'entity_type': 'GPE'},
        #     {'name': 'Vietnam', 'entity_type': 'GPE'}
        # ]
        # triples = [
        #     {
        #         'subject': 'Hoang Sa', 'relation': 'IN', 'object': 'Vietnam',
        #         'subject_entity': [('Hoang Sa', 0, 13, 'GPE')],
        #         'object_entity': [('Vietnam', 0, 13, 'GPE')]
        #     },
        # ]
        extract_info = self.extractInfo.extractTriple(query)
        triples = extract_info['triples'] if "triples" in extract_info else []

        # Processing convert
        results = []
        for triple in triples:
            subject_value = triple["subject"]
            subject_entitys = triple["subject_entity"]
            object_value = triple['object']
            object_entitys = triple['object_entity']
            relation_value = triple['relation']
            if subject_value == None \
                    or object_value == None \
                    or relation_value == None \
                    or len(subject_entitys) == 0 \
                    or len(object_entitys) == 0:
                continue
            subject_entity = None
            for item in subject_entitys:
                if len(item) < 4: continue
                if item[0] == subject_value:
                    subject_entity = item
                    break
            object_entity = None
            for item in object_entitys:
                if len(item) < 4: continue
                if item[0] == object_value:
                    object_entity = item
                    break
            if subject_entity == None or object_entity == None: continue
            results.append([
                {'type': 'entity', 'label': self.check_entity_type(subject_entity[3]),
                 'value': self.normal_entity_value(subject_value)},
                {'type': 'entity', 'label': self.check_entity_type(object_entity[3]),
                 'value': self.normal_entity_value(object_value)},
                {'type': 'relation', 'label': self.check_relation_type(relation_value),
                 'value': self.normal_relation_value(None)},
                {'type': 'origin', 'label': 'sentence', "value": f"{subject_value} {relation_value} {object_value}"}
            ])
        print(f"\n\n=========={method_tag}============\n\n")
        print("Query:", query)
        print("Results:", results)
        return results

    def get_sentences_from_query(self, query):
        method_tag = "get_sentences_from_query"
        print(f"\n\n=========={method_tag}============\n\n")
        sentences = []
        graph_results = self.graph.run(query)
        while graph_results.forward():
            record = graph_results.current
            sentence = f"{record[0]} {record[1]} {record[2]}"
            sentences.append(sentence)
            print(f"sentence:{sentence}")
        return sentences

    def get_max_similar(self, query, sentences, number_top_matches=1):
        method_tag = 'get_max_similar'
        print(f"\n\n=========={method_tag}============\n\n")
        print("Query:", query)
        print("sentences:", sentences)
        print(sentences)
        sentence_embeddings = self.model.encode(sentences)
        queries = [query]
        query_embeddings = self.model.encode(queries)

        print("Semantic Search Results")

        output = []
        for query, query_embedding in zip(queries, query_embeddings):
            distances = scipy.spatial.distance.cdist([query_embedding], sentence_embeddings, "cosine")[0]

            results = zip(range(len(distances)), distances)
            results = sorted(results, key=lambda x: x[1])

            for idx, distance in results[0:number_top_matches]:
                print(sentences[idx].strip(), "(Cosine Score: %.4f)" % (1 - distance))
                output.append((sentences[idx].strip(), 1 - distance))
        return output

    def tripleEqual(self, from_triple, to_triple):
        result = type(to_triple) and len(from_triple) == len(to_triple)
        if result:
            for index in range(len(from_triple)):
                if from_triple[index] != to_triple[index]: return False
        return result

    def check_triple_valid(self, input_triple):
        # mock check valid triple
        for triple in self.triples_valid:
            if self.tripleEqual(triple, input_triple): return input_triple
        return None

    def build_striple_misc(self, objects):
        results = []
        for triple in self.triples_valid:
            marked = []
            for index in range(len(triple)): marked.append(None)
            for entity in objects:
                if entity['label'] == "origin": continue
                indexs = self.allIndexOf(entity['label'], triple)
                if len(indexs) == 0: continue
                for index in indexs:
                    if marked[index] != None: continue
                    marked[index] = entity
                    break
            if None in marked: continue
            exist = False
            # for result in results:
            #     _triple = result[0]
            #     if tripleEqual(_triple, _triple):
            #         exist = True
            #         break
            if exist == False:
                results.append((triple, marked))  # results.append([list(a) for a in zip(triple, marked)])
        return results

    def triple_to_query(self, triple_value_tuple):
        method_tag = "triple_to_query"
        print(f"\n\n=========={method_tag}============\n\n")
        query = ''
        triple = triple_value_tuple[0]
        values = triple_value_tuple[1]
        if (len(triple) != len(values)): return query
        if self.check_triple_valid(triple) == None: return query
        if len(triple) != 3: return query
        limit_query = 10
        from_entity = triple[0]
        from_entity_value = values[0]
        to_entity = triple[1]
        to_entity_value = values[1]
        relation = triple[-1]

        query = f"MATCH (a:{from_entity})-[arc:{relation}]->(b:{to_entity}) " \
                f"WHERE a.name =~ '(?i){from_entity_value['value']}' and b.name =~ '(?i){to_entity_value['value']}' " \
                f"RETURN a.name, type(arc), b.name " \
                f" LIMIT {limit_query}"
        print(f"query:{query}")
        return query

    def process_text(self, input):
        print("\n\n======================\n\n")
        print("Input:", input)
        extract_information_datas = self.extract_information(input)
        origins = []
        weights = []
        results = []
        graph_sentences_generated = []
        for extract_information_data in extract_information_datas:
            origins.append(extract_information_data[-1]['value'])
            output = self.build_striple_misc(extract_information_data)
            sentences = set()
            for item in output:
                query = self.triple_to_query(item)
                _sentences = self.get_sentences_from_query(query)
                for item in _sentences: sentences.add(item)
            graph_sentences_generated.append(list(sentences))

        # TODO update weight
        len_origins = len(origins)
        default_weight = 1.0 / len_origins
        for index in range(len_origins):
            weights.append(default_weight)

        print(f"\n\n==========RESULTS_EXTRACT============\n\n")
        print(f"origins:{origins}")
        print(f"graph_sentences_generated:{graph_sentences_generated}")

        print(f"\n\n==========START_CHECKED============\n\n")
        for index in range(len(origins)):
            origin = origins[index]
            graph_sentence_generated = graph_sentences_generated[index]
            print(f"\n[CHECKING]{origin}===>{graph_sentence_generated}\n")
            similars = self.get_max_similar(origin, graph_sentence_generated, 1)
            result = None
            selected_sentence = None
            max_value = 0.0
            if (len(similars) > 0):
                result = similars[0]
            else:
                count = 0
                for s in graph_sentence_generated:
                    if s == origin: count = count + 1
                result = (origin, count * default_weight)
            if len(result) >= 2:
                selected_sentence = result[0]
                max_value = result[1]
            results.append(result)
            print(f"\n[CHECKING]{origin}==>{selected_sentence}:{max_value}\n")
            print(f"\n[CHECKING]{origin}[END]\n")

        print(f"\n\n==========RESULT============\n\n")
        print(f"\n[INPUT]:{input}\n")
        for index in range(len(origins)):
            print(f"\n[SENTENCE]:{origins[index]}:[weight:{weights[index]}]\n")
        combine = 0.0
        for index in range(len(origins)):
            combine = combine + weights[index] * results[index][1]
        print(f"\n[COMBINE]:{combine}\n")
        print(f"\n\n==========END============\n\n")
        output = list(zip(origins, weights, results))
        return (output, combine)

if __name__ == '__main__':
    print(f'GraphSearch')
    pass

