import uuid
import xml.dom.minidom

#输入网的名称，库所，变迁，关联矩阵，构造pnml格式的petri网
class PNML():
    def __init__(self, net_name, places, transitions, incidenceMatrix):
        self.net_id = str(uuid.uuid4())
        self.net_name = net_name

        self.places = places
        self.transitions = transitions
        self.incidenceMatrix = incidenceMatrix
        self.places_id = {}
        self.transitions_id = {}

        self.get_pnml_base()
        self.add_place()
        self.add_transitions()
        self.add_arc()

    def get_pnmlString(self):

        xml_string = self.doc.toprettyxml(indent='\t', encoding='ISO-8859-1')
        return xml_string.decode()

    def get_pnml_base(self):

        self.doc = xml.dom.minidom.Document()
        self.pnml = self.doc.createElement('pnml')
        self.net = self.doc.createElement('net')
        self.net.setAttribute('id', self.net_id)
        self.net.setAttribute('type', "http://www.yasper.org/specs/epnml-1.1")

        name = self.doc.createElement('name')
        text = self.doc.createElement('text')
        text.appendChild(self.doc.createTextNode(self.net_name))

        name.appendChild(text)
        self.net.appendChild(name)
        self.pnml.appendChild(self.net)
        self.doc.appendChild(self.pnml)
    def add_place(self):

        for item in self.places:
            place_id = str(uuid.uuid4())
            self.places_id[str(item)] = place_id
            place = self.doc.createElement('place')
            place.setAttribute('id',place_id)
            name = self.doc.createElement('name')
            text = self.doc.createElement('text')

            text.appendChild(self.doc.createTextNode(str(item)))
            name.appendChild(text)
            place.appendChild(name)
            self.net.appendChild(place)

    def  add_transitions(self):

        for item in self.transitions:
            transition_id = str(uuid.uuid4())
            self.transitions_id[item] = transition_id
            transition = self.doc.createElement('transition')
            transition.setAttribute('id', transition_id)
            name = self.doc.createElement('name')
            text = self.doc.createElement('text')

            text.appendChild(self.doc.createTextNode(item))
            name.appendChild(text)
            transition.appendChild(name)
            self.net.appendChild(transition)
    def add_arc(self):

        row = self.incidenceMatrix.shape[0]
        column = self.incidenceMatrix.shape[1]

        for i in range(row):
            for j in range(column):
                if self.incidenceMatrix[i][j]==0:
                    continue

                arc_id = str(uuid.uuid4())
                arc = self.doc.createElement('arc')
                arc.setAttribute('id', arc_id)
                text = self.doc.createElement('text')

                if self.incidenceMatrix[i][j] == 1:
                    # a arc from the jst transition to the ist place
                    arc_id = str(uuid.uuid4())
                    arc = self.doc.createElement('arc')
                    arc.setAttribute('id', arc_id)
                    text = self.doc.createElement('text')

                    text.appendChild(self.doc.createTextNode('in'))
                    arc.setAttribute('source', self.transitions_id[self.transitions[j]])
                    arc.setAttribute('target', self.places_id[str(self.places[i])])

                    name = self.doc.createElement('name')
                    name.appendChild(text)
                    arctype = self.doc.createElement('arctype')
                    text = self.doc.createElement('text')
                    text.appendChild(self.doc.createTextNode('normal'))
                    arctype.appendChild(text)

                    arc.appendChild(name)
                    arc.appendChild(arctype)
                    self.net.appendChild(arc)
                elif self.incidenceMatrix[i][j] == -1:
                    # a arc from the ist place to the jst transition
                    arc_id = str(uuid.uuid4())
                    arc = self.doc.createElement('arc')
                    arc.setAttribute('id', arc_id)
                    text = self.doc.createElement('text')

                    text.appendChild(self.doc.createTextNode('out'))
                    arc.setAttribute('target', self.transitions_id[self.transitions[j]])
                    arc.setAttribute('source', self.places_id[str(self.places[i])])

                    name = self.doc.createElement('name')
                    name.appendChild(text)
                    arctype = self.doc.createElement('arctype')
                    text = self.doc.createElement('text')
                    text.appendChild(self.doc.createTextNode('normal'))
                    arctype.appendChild(text)

                    arc.appendChild(name)
                    arc.appendChild(arctype)
                    self.net.appendChild(arc)
                else:
                    # a arc from the jst transition to the ist place
                    arc_id = str(uuid.uuid4())
                    arc = self.doc.createElement('arc')
                    arc.setAttribute('id', arc_id)
                    text = self.doc.createElement('text')

                    text.appendChild(self.doc.createTextNode('in'))
                    arc.setAttribute('source', self.transitions_id[self.transitions[j]])
                    arc.setAttribute('target', self.places_id[str(self.places[i])])

                    name = self.doc.createElement('name')
                    name.appendChild(text)
                    arctype = self.doc.createElement('arctype')
                    text = self.doc.createElement('text')
                    text.appendChild(self.doc.createTextNode('normal'))
                    arctype.appendChild(text)

                    arc.appendChild(name)
                    arc.appendChild(arctype)
                    self.net.appendChild(arc)
                    # a arc from the ist place to the jst transition
                    arc_id = str(uuid.uuid4())
                    arc = self.doc.createElement('arc')
                    arc.setAttribute('id', arc_id)
                    text = self.doc.createElement('text')

                    text.appendChild(self.doc.createTextNode('out'))
                    arc.setAttribute('target', self.transitions_id[self.transitions[j]])
                    arc.setAttribute('source', self.places_id[str(self.places[i])])

                    name = self.doc.createElement('name')
                    name.appendChild(text)
                    arctype = self.doc.createElement('arctype')
                    text = self.doc.createElement('text')
                    text.appendChild(self.doc.createTextNode('normal'))
                    arctype.appendChild(text)

                    arc.appendChild(name)
                    arc.appendChild(arctype)
                    self.net.appendChild(arc)