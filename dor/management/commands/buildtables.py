from django.core.management.base import BaseCommand, CommandError
from dor.models import Taxonomy, Standards, ContentType
from pprint import pprint

def build_taxonomy():
    for tax in INDEX_TERMS:
        root = Taxonomy.add_root(name=tax, tax_id=int(tax.split()[0]))
        for field in INDEX_TERMS[tax]:
            node_x = root.add_child(name=field, tax_id=int(field.split()[0]))
            for subfield in INDEX_TERMS[tax][field]:
                node_y = node_x.add_child(name=subfield, tax_id=int(subfield.split()[0]))
                for subj in INDEX_TERMS[tax][field][subfield]:
                    node_z = node_y.add_child(name=subj, tax_id=int(subj.split()[0]))
                    while bool(INDEX_TERMS[tax][field][subfield][subj]):
                        datatype = node_z.add_child(name=INDEX_TERMS[tax][field][subfield][subj].pop())

    print(Taxonomy.dump_bulk())


def build_standards():
    for std in STANDARDS:
        root = Standards.add_root(name=std)
        for option in STANDARDS[std]:
            root.add_child(name=option)

    pprint(Standards.dump_bulk())


def build_content():
    for item in CONTENT_TYPE:
        root = ContentType.add_root(name=item)
        while(bool(CONTENT_TYPE[item])):
            ext = root.add_child(name=CONTENT_TYPE[item].pop())

    pprint(ContentType.dump_bulk())


class Command(BaseCommand):
    help = 'Builds the db table for the taxonomy tree'

    def handle(self, *args, **options):
        build_taxonomy()
#        build_standards()
        build_content()


CONTENT_TYPE = {
    'Standard office documents': [],  # [file_extensions]
    'Networkbased data': [],
    'Databases': [],
    'Images': [],
    'Structured graphics': [],
    'Audiovisual data': [],
    'Scientific and statistical data formats': [],
    'Raw data': [],
    'Plain text': [],
    'Structured text': [],
    'Archived data': [],
    'Software applications': [],
    'Source code': [],
    'Configuration data': [],
    'other': [],
}

STANDARDS = {
    'databaseAccessTypes': ['open', 'restricted', 'closed'],
    'accessTypes': ['open', 'embargoed', 'restricted', 'closed'],
    'dataUploadTypes': ['open', 'restricted', 'closed'],
    'accessRestrictions': ['feeRequired', 'registration', 'other'],
    'repositoryTypes': ['disciplinary', 'institutional', 'other'],
    'providerTypes': ['dataProvider', 'serviceProvider'],
    'responsibilityTypes': ['funding', 'general', 'sponsoring', 'technical'],
    'institutionTypes': ['commercial', 'non-profit'],
    'databaseLicenseNames': ['CC', 'CC0', 'Copyrights', 'ODC', 'Public Domain', 'other'],
    'dataLicenseNames': ['CC', 'CC0', 'Copyrights', 'ODC', 'OGL', 'RL', 'Public Domain', 'other', 'none'],
    'softwareNames': ['CKAN', 'DataVerse', 'DigitalCommons', 'DSpace', 'EPrints', 'eSciDoc', 'OPUS', 'dLibra', 'other', 'unknown'],
    'apiTypes': ['API', 'FTP', 'OAI-PMH', 'REST', 'SOAP', 'SPARQL', 'SWORD', 'other'],
    'pidSystems': ['ARK', 'DOI', 'hdl', 'PURL', 'URN', 'other', 'none'],
    'certificates': ['DIN 31644', 'DINI Certificate', 'DSA', 'ISO 16363', 'ISO 16919', 'TRAC', 'WDS', 'other'],
    'syndicationTypes': ['ATOM', 'RSS'],
    'yesno': ['yes', 'no'],
    'yesnoun': ['yes', 'no', 'unknown'],
}

INDEX_TERMS = {
#    '1 Humanities and Social Sciences': {
#        '11 Humanities': {
#            '101 Ancient Cultures': {
#                '10101 Prehistory': [],
#                '10102 Classical Philology': [],
#                '10103 Ancient History': [],
#                '10104 Classical Archaeology': [],
#                '10105 Egyptology and Ancient Near Eastern Studies': [],
#            },
#            '102 History': {
#                '10201 Medieval History': [],
#                '10202 Early Modern History': [],
#                '10203 Modern and Current History': [],
#                '10204 History of Science': [],
#            },
#            '103 Fine Arts, Music, Theatre and Media Studies': {
#                '10301 Art History': [],
#                '10302 Musicology': [],
#                '10303 Theatre and Media Studies': [],
#            },
#            '104 Linguistics': {
#                '10401 General and Applied Linguistics': [],
#                '10402 Individual Linguistics': [],
#                '10403 Typology, Non-European Languages, Historical Linguistics': [],
#            },
#            '105 Literary Studies': {
#                '10501 Medieval German Literature': [],
#                '10502 Modern German Literature': [],
#                '10503 European and American Literature': [],
#                '10504 General and Comparative Literature and Cultural Studies': [],
#            },
#            '106 Non-European Languages and Cultures, Social and Cultural Anthropology, Jewish Studies and Religious Studies': {
#                '10601 Social and Cultural Anthropology and Ethnology/Folklore': [],
#                '10602 Asian Studies': [],
#                '10603 African, American and Oceania Studies': [],
#                '10604 Islamic Studies, Arabian Studies, Semitic Studies': [],
#                '10605 Religious Studies and Jewish Studies': [],
#            },
#            '107 Theology': {
#                '10701 Protestant Theology': [],
#                '10702 Roman Catholic Theology': [],
#            },
#            '108 Philosophy': {
#                '10801 History of Philosophy': [],
#                '10802 Theoretical Philosophy': [],
#                '10803 Practical Philosophy': [],
#            },
#        },
#        '12 Social and Behavioural Sciences': {
#            '109 Education Sciences': {
#                '10901 General Education and Historiy of Education': [],
#                '10902 Reasearch on Teaching, Learning and Tranining': [],
#                '10903 Research on Socialization and Educational Institutions and Professions': [],
#            },
#            '110 Psychology': {
#                '11001 General, Biological and Mathematical Psychology': [],
#                '11002 Developmental and Educational Psychology': [],
#                '11003 Social Psychology, Industrial and Organisational Psychology': [],
#                '11004 Differential Psychology, Clinical Psychology, Medical Psychology, Methodology': [],
#            },
#            '111 Social Sciences': {
#                '11101 Sociological Theory': [],
#                '11102 Empirical Social Research': [],
#                '11103 Communication Science': [],
#                '11104 Political Science': [],
#            },
#            '112 Economics': {
#                '11201 Economic Theory': [],
#                '11202 Economic and Social Policy': [],
#                '11203 Public Finance': [],
#                '11204 Business Administration': [],
#                '11205 Statistics and Econometrics': [],
#                '11206 Economic and Social History': [],
#            },
#            '113 Jurisprudence': {
#                '11301 Legal and Political Philosophy, Legal History, Legal Theory': [],
#                '11302 Private Law': [],
#                '11303 Public Law': [],
#                '11304 Criminal Law and Law of Criminal Procedure': [],
#                '11305 Criminology': [],
#            },
#        },
#    },
#    '2 Life Sciences': {
#        '21 Biology': {
#            '201 Basic Biological and Medical Research': {
#                '20101 Biochemistry': [],
#                '20102 Biophysics': [],
#                '20103 Cell Biology': [],
#                '20104 Structural Biology': [],
#                '20105 General Genetics': [],
#                '20106 Developmental Biology': [],
#                '20107 Bioinformatics and Theoretical Biology': [],
#                '20108 Anatomy': [],
#            },
#            '202 Plant Sciences': {
#                '20201 Plant Systematics and Evolution': [],
#                '20202 Plant Ecology and Ecosystem Analysis': [],
#                '20203 Inter-organismic Interactions of Plants': [],
#                '20204 Plant Physiology': [],
#                '20205 Plant Biochemistry and Biophysics': [],
#                '20206 Plant Cell and Developmental Biology': [],
#                '20207 Plant Genetics': [],
#            },
#            '203 Zoology': {
#                '20301 Systematics and Morphology': [],
#                '20302 Evolution, Anthropology': [],
#                '20303 Animal Ecology, Biodiversity and Ecosystem Research': [],
#                '20304 Sensory and Behavioural Biology': [],
#                '20305 Biochemistry and Animal Physiology': [],
#                '20306 Animal Genetics, Cell and Developmental Biology': [],
#            },
#        },
#        '22 Medicine': {
#            '204 Microbiology, Virology and Immunology': {
#                '20401 Metabolism, Biochemistry and Genetics of Microorganisms': [],
#                '20402 Microbial Ecology and Applied Microbiology': [],
#                '20403 Medical Microbiology, Molecular Infection Biology': [],
#                '20404 Virology': [],
#                '20405 Immunology': [],
#            },
#            '205 Medicine': {
#                '20501 Epidemiology, Medical Biometry, Medical Informatics': [],
#                '20502 Public Health, Health Services Research, Social Medicine': [],
#                '20503 Human Genetics': [],
#                '20504 Physiology': [],
#                '20505 Nutritional Sciences': [],
#                '20506 Pathology and Forensic Medicine': [],
#                '20507 Clinical Chemistry and Pathobiochemistry': [],
#                '20508 Pharmacy': [],
#                '20509 Pharmacology': [],
#                '20510 Toxicology and Occupational Medicine': [],
#                '20511 Anaesthesiology': [],
#                '20512 Cardiology, Angiology': [],
#                '20513 Pneumology, Clinical Infectiology Intensive Care Medicine': [],
#                '20514 Hematology, Oncology, Transfusion Medicine': [],
#                '20515 Gastroenterology, Metabolism': [],
#                '20516 Nephrology': [],
#                '20517 Endocrinology, Diabetology': [],
#                '20518 Rheumatology, Clinical Immunology, Allergology': [],
#                '20519 Dermatology': [],
#                '20520 Pediatric and Adolescent Medicine': [],
#                '20521 Gynaecology and Obstetrics': [],
#                '20522 Reproductive Medicine/Biology': [],
#                '20523 Urology': [],
#                '20524 Gerontology and Geriatric Medicine': [],
#                '20525 Vascular and Visceral Surgery': [],
#                '20526 Cardiothoracic Surgery': [],
#                '20527 Traumatology and Orthopaedics': [],
#                '20528 Dentistry, Oral Surgery': [],
#                '20529 Otolaryngology': [],
#                '20530 Radiology and Nuclear Medicine': [],
#                '20531 Radiation Oncology and Radiobiology': [],
#                '20532 Biomedical Technology and Medical Physics': [],
#            },
#            '206 Neurosciences': {
#                '20601 Molecular Neuroscience and Neurogenetics': [],
#                '20602 Cellular Neuroscience': [],
#                '20603 Developmental Neurobiology': [],
#                '20604 Systemic Neuroscience, Computational Neuroscience, Behaviour': [],
#                '20605 Comparative Neurobiology': [],
#                '20606 Cognitive Neuroscience and Neuroimaging': [],
#                '20607 Molecular Neurology': [],
#                '20608 Clinical Neurosciences I - Neurology, Neurosurgery': [],
#                '20609 Biological Psychiatry': [],
#                '20610 Clinical Neurosciences II - Psychotherapy, Psychosomatic Medicine': [],
#                '20611 Clinical Neurosciences III - Ophthalmology': [],
#            },
#        },
#        '23 Agriculture, Forestry, Horticulture and Veterinary Medicine': {
#            '207 Agriculture, Forestry, Horticulture and Veterinary Medicine': {
#                '20701 Soil Sciences': [],
#                '20702 Plant Cultivation': [],
#                '20703 Plant Nutrition': [],
#                '20704 Ecology of Agricultural Landscapes': [],
#                '20705 Plant Breeding': [],
#                '20706 Phytomedicine': [],
#                '20707 Agricultural and Food Process Engineering': [],
#                '20708 Agricultural Economics and Sociology': [],
#                '20709 Inventory Control and Use of Forest Resources': [],
#                '20710 Basic Forest Research': [],
#                '20711 Animal Husbandry, Breeding and Hygiene': [],
#                '20712 Animal Nutrition and Nutrition Physiology': [],
#                '20713 Basic Veterinary Medical Science': [],
#                '20714 Basic Research on Pathogenesis, Diagnostics and Therapy and Clinical Vererinary Medicine': [],
#            },
#        },
#    },
#    '3 Natural Sciences': {
#        '31 Chemistry': {
#            '301 Molecular Chemistry': {
#                '30101 Inorganic Molecular Chemistry': [],
#                '30102 Organic Molecular Chemistry': [],
#            },
#            '302 Chemical Solid State and Surface Research': {
#                '30201 Solid State and Surface Chemistry, Material Synthesis': [],
#                '30202 Physical Chemistry of Solids and Surfaces, Material Charaacterisation': [],
#                '30203 Theory and Modelling': [],
#            },
#            '303 Physical and Theoretical Chemistry': {
#                '30301 Physical Chemistry of Molecules, Interfaces and Liquids - Spectroscopy, Kinetics': [],
#                '30302 General Theoretical Chemistry': [],
#            },
#            '304 Analytical Chemistry, Method Development (Chemistry)': {
#                '30401 Analytical Chemistry, Method Development (Chemistry)': [],
#            },
#            '305 Biological Chemistry and Food Chemistry': {
#                '30501 Biological and Biomimetic Chemistry': [],
#                '30502 Food Chemistry': [],
#            },
#            '306 Polymer Research': {
#                '30601 Preparatory and Physical Chemistry of Polymers': [],
#                '30602 Experimental and Theoretical Physics of Polymers': [],
#                '30603 Polymer Materials': [],
#            },
#        },
#        '32 Physics': {
#            '307 Condensed Matter Physics': {
#                '30701 Experimental Condensed Matter Physics': [],
#                '30702 Theoretical Condensed Matter Physics': [],
#            },
#            '308 Optics, Quantum Optics and Physics of Atoms, Molecules and Plasmas': {
#                '30801 Optics, Quantum Optics, Atoms, Molecules, Plasmas': [],
#            },
#            '309 Particles, Nuclei and Fields': {
#                '30901 Particles, Nuclei and Fields': [],
#            },
#            '310 Statistical Physics, Soft Matter, Biological Physics, Nonlinear Dynamics': {
#                '31001 Statistical Physics, Soft Matter, Biological Physics, Nonlinear Dynamics': [],
#            },
#            '311 Astrophysics and Astronomy': {
#                '31101 Astrophysics and Astronomy': [],
#            },
#        },
#        '33 Mathematics': {
#            '312 Mathematics': {
#                '31201 Mathematics': [],
#            },
#        },
#        '34 Geosciences (including Geography)': {
#            '313 Atmospheric Science and Oceanography': {
#                '31301 Atmospheric Science': [],
#                '31302 Oceanography': [],
#            },
#            '314 Geology and Palaeontology': {
#                '31401 Geology and Palaeontology': [],
#            },
#            '315 Geophysics and Geodesy': {
#                '31501 Geophysics': [],
#                '31502 Geodesy, Photogrammetry, Remote Sensing, Geoinformatics, Cartogaphy': [],
#            },
#            '316 Geochemistry, Mineralogy and Crystallography': {
#                '31601 Geochemistry, Mineralogy and Crystallography': [],
#            },
#            '317 Geography': {
#                '31701 Physical Geography': [],
#                '31702 Human Geography': [],
#            },
#            '318 Water Research': {
#                '31801 Hydrogeology, Hyddrology, Limnology, Urban Water Management, Water Chemistry, Integrated Water Resources Management': [],
#            },
#        },
#    },
#    '4 Engineering Sciences': {
#        '41 Mechanical and industrial Engineering': {
#            '401 Production Technology': {
#                '40101 Metal-Cutting Manufacturing Engineering': [],
#                '40102 Primary Shaping and Reshaping Technology': [],
#                '40103 Micro-, Precision, Mounting, Joining, Separation Techn': [],
#                '40104 Plastics Engineering': [],
#                '40105 Production Automation, Factory Operation, Operations Manangement': [],
#            },
#            '402 Mechanics and Constructive Mechanical Engineering': {
#                '40201 Construction, Machine Elements': [],
#                '40202 Mechanics': [],
#                '40203 Lightweight Construction, Textile Technology': [],
#                '40204 Acoustics': [],
#            },
#        },
#        '42 Thermal Engineering/Process Engineering': {
#            '403 Process Engineering, Technical Chemistry': {
#                '40301 Chemical and Thermal Process Engineering': [],
#                '40302 Technical Chemistry': [],
#                '40303 Mechanical Process Engineering': [],
#                '40304 Biological Process Engineering': [],
#            },
#            '404 Heat Energy Technology, Thermal Machines, Fluid Mechanics': {
#                '40401 Energy Process Engineering': [],
#                '40402 Technical Thermodynamics': [],
#                '40403 Fluid Mechanics': [],
#                '40404 Hydraulic and Turbo Engines and Piston Engines': [],
#            },
#        },
#        '43 Materials Science and Engineering': {
#            '405 Materials Engineering': {
#                '40501 Metallurgical and Thermal Processes, Thermomechanical Treatment of Materials': [],
#                '40502 Sintered Metallic and Ceramic Materials': [],
#                '40503 Composite Materials': [],
#                '40504 Mechanical Behaviour of Construction Materials': [],
#                '40505 Coating and Surface Technology': [],
#            },
#            '406 Materials Science': {
#                '40601 Thermodynamics and Kinetics of Materials': [],
#                '40602 Synthesis and Properties of Functional Materials': [],
#                '40603 Microstructural Mechanical Properties of Materials': [],
#                '40604 Structuring and Functionalisation': [],
#                '40605 Biomaterials': [],
#            },
#        },
#        '44 Computer Science, Electrical and System Engineering': {
#            '407 Systems Engineering': {
#                '40701 Automation, Control Systems, Robotics, Mechatronics': [],
#                '40702 Measurement Systems': [],
#                '40703 Microsystems': [],
#                '40704 Traffic and Transport Systems, Logistics': [],
#                '40705 Human Factors, Ergonomics, Human-Machine Systems': [],
#            },
#            '408 Electrical Engineering': {
#                '40801 Electronic Semiconductors, Components, Circuits, Systems': [],
#                '40802 Communication, High-Frequency and Network Technology, Theoretical ElectricalEngineering': [],
#                '40803 Electrical Energy Generation, Distribution, Application': [],
#            },
#            '409 Computer Science': {
#                '40901 Theoretical Computer Science': [],
#                '40902 Software Technology': [],
#                '40903 Operating, Communication and Information Systems': [],
#                '40904 Artificial Intelligence, Image and Language Processing': [],
#                '40905 Computer Architecture and Embedded Systems': [],
#            },
#        },
#        '45 Construction Engineering and Architecture': {
#            '410 Construction Engineering and Architecture': {
#                '41001 Architecture, Building and Construction History, Sustainable Building Technology, Building Design': [],
#                '41002 Urbanism, Spatial Planning, Transportation and Infrastructure Planning, Landscape Planning': [],
#                '41003 Construction Material Sciences, Chemistry, Building Physics': [],
#                '41004 Sructural Engineering, Building Informatics, Construction Operation': [],
#                '41005 Applied Mechanics, Statics and Dynamics': [],
#                '41006 Geotechnics, Hydraulic Engineering': [],
#            },
#        },
#    },
    ############### AGU Terms ###############
    '1 All Terms': {
        '51 Geoscience': {
            '501 Antarctic and Arctic Sciences': {
                '50101 Antarctic Science': [],
                '50102 Arctic Science': [],
                '50103 Antarctic astronomy ': [],
                '50104 Cryosphere': [],
                '50105 Polar atmospheric science ': [],
                '50106 Polar biology and ecology ': [],
                '50107 Polar engineering ': [],
                '50108 Polar Geography': [],
                '50109 Polar geology ': [],
                '50110 Polar geophysics': [],
                '50111 Polar geochemistry ': [],
                '50112 Polar glaciology': [],
                '50113 Polar oceanography': [],
                '50114 Polar space physics': [],
            },
            '502 Atmospheric Sciences': {
                '50201 Aeronomy': [],
                '50202 Air Quality': [],
                '50203 Atmospheric Chemistry': [],
                '50204 Atmospheric Modeling': [],
                '50205 Atmospheric Physics': [],
                '50206 Atmospheric Science': [],
                '50207 Heliophysics': [],
                '50208 Meteorology': [],
            },
            '503 Climate Science': {
                '50301 Climate Geography': [],
                '50302 Climate Science': [],
                '50303 Earth System Modeling': [],
                '50304 Climate Simulation': [],
                '50305 Global climate change': [],
            },
            '504 Geochemistry': {
                '50401 Biogeochemistry': [],
                '50402 Geochemistry': [],
                '50403 High Temperature Geochemistry': [],
                '50404 Igneous Petrology': [],
                '50405 Low temperature geochemistry': [],
                '50406 Metamorphic Petrology': [],
                '50407 Mineralogy': [],
                '50408 Petrology': [],
                '50409 Volcanology': [],
            },
            '505 Geology': {
                '50501 Geochronology': [],
                '50502 Geology': [],
                '50503 Geomorphology': [],
                '50504 Glaciology': [],
                '50505 Sedimentology': [],
                '50506 Stratigraphy': [],
                '50507 Structural Geology ': [],
                '50508 Tectonics': [],
            },
            '506 Geophysics': {
                '50601 Active Tectonics': [],
                '50602 Geodesy': [],
                '50603 Geodynamics': [],
                '50604 Geophysics': [],
                '50605 Magnetism ': [],
                '50606 Mineral Physics': [],
                '50607 Near Surface Geophysics': [],
                '50608 Potential Fields and Heat Flow': [],
                '50609 Rock Mechanics': [],
                '50610 Seismology': [],
            },
            '507 Hydrology': {
                '50701 Hydrology': [],
                '50702 Hydrogeosciences': [],
                '50703 Groundwater ': [],
                '50704 Watershed dynamics': [],
                '50705 Water Resources': [],
                '50706 Water Cycle': [],
                '50707 Water Quality': [],
            },
            '508 Oceanography': {
                '50801 Biological Oceanography': [],
                '50802 Chemical Oceanography': [],
                '50803 Coastal and Marine Geography': [],
                '50804 Coastal Processes': [],
                '50805 Limnology': [],
                '50806 Marine Geochemistry': [],
                '50807 Marine Geology and Geophysics': [],
                '50808 Marine Microbiology': [],
                '50809 Ocean omics': [],
                '50810 Ocean biogeochemistry': [],
                '50811 Ocean Ecology': [],
                '50812 Ocean Modeling and Simulation': [],
                '50813 Oceanography': [],
                '50814 Physical Oceanography': [],
            },
            '509 Paleogeosciences': {
                '50901 Paleontology': [],
                '50902 Paleobiology': [],
                '50903 Paleoclimate': [],
                '50904 Paleoenvironmental Change': [],
                '50905 Paleogeology': [],
                '50906 Paleogeoscience': [],
                '50907 Paleomagnetism': [],
                '50908 Paleooceanography': [],
                '50909 Paleontology': [],
                '50910 Paleoseismology': [],
            },
            '510 Space Physics and Planetary Science': {
                '51001 Aeronomy': [],
                '51002 Astronomy': [],
                '51003 Heliophysics': [],
                '51004 Radio Astronomy': [],
                '51005 Space Physics': [],
                '51006 Space Weather': [],
            },
        },
        '52 Interdisciplinary': {
            '511 Biology/Ecosystems Science': {
                '51101 Biology': [],
                '51102 Biodiversity': [],
                '51103 Biogeography ': [],
                '51104 Biogeoscience': [],
                '51105 Ecology': [],
                '51106 Ecosystem Science': [],
                '51107 Environmental Resource Management': [],
                '51108 Geobiology': [],
                '51109 Geomicrobiology': [],
                '51110 Microbial Studies': [],
                '51111 Population Studies': [],
            },
            '512 Critical Zone Science': {
                '51201 Agronomy': [],
                '51202 Critical Zone Science': [],
            },
            '513 Natural Hazards': {
                '51301 Cyclones': [],
                '51302 Earthquakes': [],
                '51303 Fires': [],
                '51304 Floods': [],
                '51305 Hurricanes': [],
                '51306 Landslides': [],
                '51307 Tornados': [],
                '51308 Tsunami': [],
                '51309 Volcanic Eruptions': [],
                '51310 Others': [],
            },
            '514 Physical Geography': {
                '51401 Geospatial Studies': [],
                '51402 Geographic Information Science and Systems': [],
                '51403 Physical Geography': [],
                '51404 Spatial Analysis and Modeling': [],
            },
            '515 Social Sciences': {
                '51501 Anthropology': [],
                '51502 Economics': [],
                '51503 Economic Geology': [],
                '51504 Human Geography': [],
                '51505 Information Science': [],
                '51506 Institutional/Organizational Studies': [],
                '51507 Political Science': [],
                '51508 Psychology': [],
            },
        },
        '53 Cyberinfrastructure and Computer Sciences': {
            '516 Computer Science': {
                '51601 Algorithms': [],
                '51602 Computational Science': [],
                '51603 Computer Science': [],
                '51604 Geographic Information Science': [],
                '51605 Modeling': [],
                '51606 Numerical Modeling': [],
                '51607 Risk Modeling': [],
                '51608 Visualization Sciences': [],
            },
            '517 Cyberinfrastructure': {
                '51701 Cyberinfrastructure and Hardware Engineer': [],
                '51702 Geoinformatics': [],
                '51703 High Performance Computing': [],
                '51704 Informatics/Information Systems': [],
                '51705 System Design': [],
            },
            '518 Data manager/data services': {
                '51801 Data Management ': [],
                '51802 Data Science': [],
                '51803 Data Services/Assimilation': [],
                '51804 Disaster Assessment': [],
                '51805 Remote Sensing': [],
                '51806 Satellite Processing': [],
                '51807 System Integration': [],
                '51808 User Support': [],
            },
            '519 Software engineering': {
                '51901 Software Engineering': [],
                '51902 Programming': [],
            },
        },
    },
}
