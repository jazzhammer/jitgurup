import os

from django.apps import AppConfig
from django.forms import model_to_dict
from dotenv import load_dotenv



load_dotenv()


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        print(f"============================================================")
        print(f"""
                      .__                       _____.__
        _____  ______ |__|   ____  ____   _____/ ____\\__| ____
        \\__  \\ \\____ \\|  | _/ ___\\/  _ \\ /    \\   __\\|  |/ ___| 
         / __ \\|  |_> >  | \\  \\__(  <_> )   |  \\  |  |  / /_/  >
        (____  /   __/|__|  \\___  >____/|___|  /__|  |__\\___  /
             \\/|__|             \\/           \\/        /_____/
        """)
        print(f"------------------------------------------------------------")

        self.confirm_default_users()
        self.confirm_default_subjects()
        self.confirm_default_orgs()
        self.confirm_user_orgs()
        self.confirm_learning_modalitys()
        self.confirm_preferred_modalitys()
        self.confirn_default_groups()
        self.confirm_default_roles()
        # self.confirmDefaultPermissions()
        # self.confirmDefaultGroupPermissions()


    def confirm_default_role(self, name: str):
        from api.models.role import Role
        if len(Role.objects.filter(name__iexact=name)) == 0:
            return Role.objects.create(name=name)

    def confirm_default_roles(self):
        self.confirm_default_role('guru')
        self.confirm_default_role('pupil')
        self.confirm_default_role('observer')


    def confirm_preferred_modalitys(self):
        from api.models.person import Person
        from api.models.learning_modality import LearningModality
        from api.models.topic import Topic
        import random

        guru_a = Person.objects.get(last_name="guru_a")
        guru_b = Person.objects.get(last_name="guru_b")
        guru_c = Person.objects.get(last_name="guru_c")

        learning_modalitys = LearningModality.objects.all()
        topics_to_assign = random.choices(Topic.objects.all(), k=20)

        for learning_modality in learning_modalitys:
            for topic in topics_to_assign:
                self.confirm_preferred_modality(guru_a, topic, learning_modality)

        for learning_modality in learning_modalitys:
            for topic in topics_to_assign:
                self.confirm_preferred_modality(guru_b, topic, learning_modality)

        for learning_modality in learning_modalitys:
            for topic in topics_to_assign:
                self.confirm_preferred_modality(guru_c, topic, learning_modality)

    def confirm_preferred_modality(self, person, topic, learning_modality):
        from api.models.preferred_modality import PreferredModality

        already = PreferredModality.objects.filter(person=person, topic=topic, learning_modality=learning_modality)
        if len(already) == 0:
            created = PreferredModality.objects.create(person=person, topic=topic, learning_modality=learning_modality)

    def confirm_learning_modalitys(self):
        confirmed = self.confirm_learning_modality('1:1')
        confirmed = self.confirm_learning_modality('lecture')
        confirmed = self.confirm_learning_modality('workshop')
        confirmed = self.confirm_learning_modality('self_study')
        confirmed = self.confirm_learning_modality('studio')

    def confirm_learning_modality(self, name: str):
        from api.models.learning_modality import LearningModality
        already = LearningModality.objects.filter(name__iexact=name)
        if len(already) == 0:
            created = LearningModality.objects.create(name=name)
            return created

    def confirm_default_subject(self, name: str):
        from api.models.subject import Subject

        alreadys = Subject.objects.filter(name__iexact=name)
        if len(alreadys) == 0:
            created = Subject.objects.create(name=name)
            return created
        return alreadys[0]

    def confirm_default_topic(self, subject, name: str):
        from api.models.topic import Topic

        alreadys = Topic.objects.filter(subject=subject, name__iexact=name)
        if len(alreadys) == 0:
            created = Topic.objects.create(subject=subject, name=name)
            return created
        return alreadys[0]

    def confirm_default_subjects(self):
        self.confirm_default_subject('Applied & Natural Sciences')
        self.confirm_default_subject('Programs')
        self.confirm_default_subject('Courses')
        self.confirm_default_subject('Business & Media')
        self.confirm_default_subject('Computing & IT')
        self.confirm_default_subject('Engineering')
        self.confirm_default_subject('Health')
        self.confirm_default_subject('Sciences')

        self.confirm_default_subject('Business')
        self.confirm_default_subject('Education')
        self.confirm_default_subject('Environment & Agriculture')
        self.confirm_default_subject('Fine Arts')
        self.confirm_default_subject('Humans & Culture')
        self.confirm_default_subject('Indigenous Topics')
        self.confirm_default_subject('Math & Technology')

        subject = self.confirm_default_subject('Accounting')
        self.confirm_default_topic(subject,'Financial Statements')
        self.confirm_default_topic(subject,'Accounting Principles and concepts')
        self.confirm_default_topic(subject,'Double-entry accounting')
        self.confirm_default_topic(subject,'Recording transactions')
        self.confirm_default_topic(subject,'Adjusting transactions')
        self.confirm_default_topic(subject,'Financial statement analysis')
        self.confirm_default_topic(subject,'Revenue Recognition')
        self.confirm_default_topic(subject,'Expense Recognition')
        self.confirm_default_topic(subject,'Inventory Valuation')
        self.confirm_default_topic(subject,'Depreciation and Amortisation')

        subject = self.confirm_default_subject('Addictions and Mental Health')

        self.confirm_default_topic(subject, 'Defining addiction and key characteristics')
        self.confirm_default_topic(subject, 'Neurobiology of addiction')
        self.confirm_default_topic(subject, 'The cycle of addiction')
        self.confirm_default_topic(subject, 'Risk factors for addiction')
        self.confirm_default_topic(subject, 'Substance use disorders:')
        self.confirm_default_topic(subject, 'Alcohol use disorder')
        self.confirm_default_topic(subject, 'Opioid use disorder')
        self.confirm_default_topic(subject, 'Stimulant use disorder')
        self.confirm_default_topic(subject, 'Cannabis use disorder')
        self.confirm_default_topic(subject, 'Tobacco use disorder')
        self.confirm_default_topic(subject, 'Co-occurring mental health disorders:')
        self.confirm_default_topic(subject, 'Depression and addiction')
        self.confirm_default_topic(subject, 'Anxiety and addiction')
        self.confirm_default_topic(subject, 'PTSD and addiction')
        self.confirm_default_topic(subject, 'Bipolar disorder and addiction')
        self.confirm_default_topic(subject, 'Assessment and screening:')
        self.confirm_default_topic(subject, 'Identifying signs and symptoms of addiction')
        self.confirm_default_topic(subject, 'Standardized screening tools')
        self.confirm_default_topic(subject, 'Conducting comprehensive assessments')
        self.confirm_default_topic(subject, 'Treatment approaches:')
        self.confirm_default_topic(subject, 'Individual therapy (CBT, motivational interviewing)')
        self.confirm_default_topic(subject, 'Group therapy')
        self.confirm_default_topic(subject, 'Family therapy')
        self.confirm_default_topic(subject, 'Medication-assisted treatment')
        self.confirm_default_topic(subject, 'Harm reduction strategies')
        self.confirm_default_topic(subject, 'Recovery management:')
        self.confirm_default_topic(subject, 'Relapse prevention planning')
        self.confirm_default_topic(subject, 'Coping skills development')
        self.confirm_default_topic(subject, 'Maintaining sobriety')
        self.confirm_default_topic(subject, 'Special populations:')
        self.confirm_default_topic(subject, 'Adolescent addiction')
        self.confirm_default_topic(subject, 'Older adults and substance use')
        self.confirm_default_topic(subject, 'LGBTQ+ individuals and addiction')
        self.confirm_default_topic(subject, 'Social and cultural considerations:')
        self.confirm_default_topic(subject, 'Stigma associated with addiction')
        self.confirm_default_topic(subject, 'Impact of socioeconomic factors on addiction')
        self.confirm_default_topic(subject, 'Cultural influences on substance use patterns')
        self.confirm_default_topic(subject, 'Legal and ethical issues:')
        self.confirm_default_topic(subject, 'Confidentiality and privacy')
        self.confirm_default_topic(subject, 'Mandatory reporting requirements')
        self.confirm_default_topic(subject, 'Ethical decision-making in addiction treatment')

        subject = self.confirm_default_subject('Counselling')

        self.confirm_default_topic(subject, 'Depression and mood disorders')
        self.confirm_default_topic(subject, 'Anxiety disorders')
        self.confirm_default_topic(subject, 'Stress management')
        self.confirm_default_topic(subject, 'Self-esteem issues')
        self.confirm_default_topic(subject, 'Grief and loss')
        self.confirm_default_topic(subject, 'Trauma')
        self.confirm_default_topic(subject, 'Anger management')
        self.confirm_default_topic(subject, 'Relationship issues:')
        self.confirm_default_topic(subject, 'Conflict resolution')
        self.confirm_default_topic(subject, 'Communication skills')
        self.confirm_default_topic(subject, 'Boundary setting')
        self.confirm_default_topic(subject, 'Intimate partner violence')
        self.confirm_default_topic(subject, 'Family dynamics')
        self.confirm_default_topic(subject, 'Parenting challenges')
        self.confirm_default_topic(subject, 'Identity and personal development:')
        self.confirm_default_topic(subject, 'Self-awareness')
        self.confirm_default_topic(subject, 'Identity development')
        self.confirm_default_topic(subject, 'Career counselling')
        self.confirm_default_topic(subject, 'Life transitions')
        self.confirm_default_topic(subject, 'Specific populations:')
        self.confirm_default_topic(subject, 'Adolescent counselling')
        self.confirm_default_topic(subject, 'Older adult counselling')
        self.confirm_default_topic(subject, 'LGBTQ+ counselling')
        self.confirm_default_topic(subject, 'Cross-cultural counselling')
        self.confirm_default_topic(subject, 'Disability counselling')
        self.confirm_default_topic(subject, 'Theoretical frameworks:')
        self.confirm_default_topic(subject, 'Cognitive Behavioral Therapy (CBT)')
        self.confirm_default_topic(subject, 'Person-centered therapy')
        self.confirm_default_topic(subject, 'Psychoanalytic theory')
        self.confirm_default_topic(subject, 'Solution-focused brief therapy')
        self.confirm_default_topic(subject, 'Systemic therapy')
        self.confirm_default_topic(subject, 'Counselling skills:')
        self.confirm_default_topic(subject, 'Active listening')
        self.confirm_default_topic(subject, 'Empathy')
        self.confirm_default_topic(subject, 'Reflection')
        self.confirm_default_topic(subject, 'Questioning techniques')
        self.confirm_default_topic(subject, 'Non-verbal communication')
        self.confirm_default_topic(subject, 'Building rapport')
        self.confirm_default_topic(subject, 'Ethical considerations:')
        self.confirm_default_topic(subject, 'Confidentiality')
        self.confirm_default_topic(subject, 'Dual relationships')
        self.confirm_default_topic(subject, 'Informed consent')
        self.confirm_default_topic(subject, 'Professional boundaries')

        subject = self.confirm_default_subject('Addictions Counselling')
        self.confirm_default_topic(subject, 'Depression and mood disorders')
        self.confirm_default_topic(subject, 'Anxiety disorders')
        self.confirm_default_topic(subject, 'Stress management')
        self.confirm_default_topic(subject, 'Self-esteem issues')
        self.confirm_default_topic(subject, 'Grief and loss')
        self.confirm_default_topic(subject, 'Trauma')
        self.confirm_default_topic(subject, 'Anger management')
        self.confirm_default_topic(subject, 'Relationship issues:')
        self.confirm_default_topic(subject, 'Conflict resolution')
        self.confirm_default_topic(subject, 'Communication skills')
        self.confirm_default_topic(subject, 'Boundary setting')
        self.confirm_default_topic(subject, 'Intimate partner violence')
        self.confirm_default_topic(subject, 'Family dynamics')
        self.confirm_default_topic(subject, 'Parenting challenges')
        self.confirm_default_topic(subject, 'Identity and personal development:')
        self.confirm_default_topic(subject, 'Self-awareness')
        self.confirm_default_topic(subject, 'Identity development')
        self.confirm_default_topic(subject, 'Career counselling')
        self.confirm_default_topic(subject, 'Life transitions')
        self.confirm_default_topic(subject, 'Specific populations:')
        self.confirm_default_topic(subject, 'Adolescent counselling')
        self.confirm_default_topic(subject, 'Older adult counselling')
        self.confirm_default_topic(subject, 'LGBTQ+ counselling')
        self.confirm_default_topic(subject, 'Cross-cultural counselling')
        self.confirm_default_topic(subject, 'Disability counselling')
        self.confirm_default_topic(subject, 'Theoretical frameworks:')
        self.confirm_default_topic(subject, 'Cognitive Behavioral Therapy (CBT)')
        self.confirm_default_topic(subject, 'Person-centered therapy')
        self.confirm_default_topic(subject, 'Psychoanalytic theory')
        self.confirm_default_topic(subject, 'Solution-focused brief therapy')
        self.confirm_default_topic(subject, 'Systemic therapy')
        self.confirm_default_topic(subject, 'Counselling skills:')
        self.confirm_default_topic(subject, 'Active listening')
        self.confirm_default_topic(subject, 'Empathy')
        self.confirm_default_topic(subject, 'Reflection')
        self.confirm_default_topic(subject, 'Questioning techniques')
        self.confirm_default_topic(subject, 'Non-verbal communication')
        self.confirm_default_topic(subject, 'Building rapport')
        self.confirm_default_topic(subject, 'Ethical considerations:')
        self.confirm_default_topic(subject, 'Confidentiality')
        self.confirm_default_topic(subject, 'Dual relationships')
        self.confirm_default_topic(subject, 'Informed consent')
        self.confirm_default_topic(subject, 'Professional boundaries')
        subject = self.confirm_default_subject('Agricultural')

        self.confirm_default_topic(subject, 'Crop physiology and development')
        self.confirm_default_topic(subject, 'Plant breeding and genetics')
        self.confirm_default_topic(subject, 'Weed management')
        self.confirm_default_topic(subject, 'Pest and disease control')
        self.confirm_default_topic(subject, 'Nutrient management')
        self.confirm_default_topic(subject, 'Crop rotation and diversification')
        self.confirm_default_topic(subject, 'Livestock Science')
        self.confirm_default_topic(subject, 'Animal nutrition and feeding')
        self.confirm_default_topic(subject, 'Animal health and reproduction')
        self.confirm_default_topic(subject, 'Animal welfare')
        self.confirm_default_topic(subject, 'Genetics and breeding programs')
        self.confirm_default_topic(subject, 'Livestock management systems')
        self.confirm_default_topic(subject, 'Soil Science')
        self.confirm_default_topic(subject, 'Soil structure and composition')
        self.confirm_default_topic(subject, 'Soil fertility and nutrient cycling')
        self.confirm_default_topic(subject, 'Soil conservation practices')
        self.confirm_default_topic(subject, 'Environmental Considerations')
        self.confirm_default_topic(subject, 'Water management and irrigation')
        self.confirm_default_topic(subject, 'Climate change impacts on agriculture')
        self.confirm_default_topic(subject, 'Sustainable farming practices')
        self.confirm_default_topic(subject, 'Organic agriculture')
        self.confirm_default_topic(subject, 'Economics and Agribusiness')
        self.confirm_default_topic(subject, 'Market analysis and pricing')
        self.confirm_default_topic(subject, 'Farm management and financial planning')
        self.confirm_default_topic(subject, 'Marketing and distribution channels')
        self.confirm_default_topic(subject, 'Technology in Agriculture')
        self.confirm_default_topic(subject, 'Precision agriculture using GPS and sensors')
        self.confirm_default_topic(subject, 'Agricultural robotics and drones')
        self.confirm_default_topic(subject, 'Data analysis and decision-making tools')

        subject = self.confirm_default_subject('Biotechnology')

        self.confirm_default_topic(subject, 'Synthetic biology')
        self.confirm_default_topic(subject, 'Transgenic plants and animals')
        self.confirm_default_topic(subject, 'Gene therapy')
        self.confirm_default_topic(subject, 'Uses of genetic engineering')
        self.confirm_default_topic(subject, 'Environmental biotechnology')
        self.confirm_default_topic(subject, 'Pharmacogenomics')
        self.confirm_default_topic(subject, 'Stem Cell Research')
        self.confirm_default_topic(subject, 'Biofuel production')
        self.confirm_default_topic(subject, 'Bioinformatics')
        self.confirm_default_topic(subject, 'Biopharmaceutical')
        self.confirm_default_topic(subject, 'Bioremediation by genetically modified microbes')
        self.confirm_default_topic(subject, 'Cloning')
        self.confirm_default_topic(subject, 'Microbial Biotechnology')
        self.confirm_default_topic(subject, 'Nanotechnology')

        subject = self.confirm_default_subject('Agricultural Studies')

        self.confirm_default_topic(subject, 'Agricultural markets')
        self.confirm_default_topic(subject, 'Animal Science')
        self.confirm_default_topic(subject, 'Sustainable agriculture')
        self.confirm_default_topic(subject, 'Agronomy')
        self.confirm_default_topic(subject, 'Farm finance')
        self.confirm_default_topic(subject, 'Horticulture')
        self.confirm_default_topic(subject, 'Botany')
        self.confirm_default_topic(subject, 'Agricultural economics')
        self.confirm_default_topic(subject, 'Agricultural engineering')
        self.confirm_default_topic(subject, 'Crop production')
        self.confirm_default_topic(subject, 'Ecology')
        self.confirm_default_topic(subject, 'Entomology')
        self.confirm_default_topic(subject, 'Food science')
        self.confirm_default_topic(subject, 'Land Industries')
        self.confirm_default_topic(subject, 'Plant physiology')
        self.confirm_default_topic(subject, 'Soil conservation')
        self.confirm_default_topic(subject, 'Soil science')

        subject = self.confirm_default_subject('Anthropology')
        self.confirm_default_topic(subject, 'Human adaptation and evolution')
        self.confirm_default_topic(subject, 'Archaeology')
        self.confirm_default_topic(subject, 'Biological anthropology')
        self.confirm_default_topic(subject, 'Forensic anthropology')
        self.confirm_default_topic(subject, 'Linguistic anthropology')
        self.confirm_default_topic(subject, 'Influence of society on mental wellness')
        self.confirm_default_topic(subject, 'The Anthropology of food')
        self.confirm_default_topic(subject, 'Cultural anthropology')
        self.confirm_default_topic(subject, 'Cultural practices and beliefs')

        subject = self.confirm_default_subject('Applied Statistics')
        self.confirm_default_topic(subject, 'Time series analysis and forecasting techniques')
        self.confirm_default_topic(subject, 'Analyzing and interpreting genomics data')
        self.confirm_default_topic(subject, 'Bayesian statistics')
        self.confirm_default_topic(subject, 'Design and Analysis of experiments')
        self.confirm_default_topic(subject, 'Analysis of variance')
        self.confirm_default_topic(subject, 'Basic statistics')
        self.confirm_default_topic(subject, 'Common distributions')
        self.confirm_default_topic(subject, 'Predictive modeling for financial risk assessment')
        self.confirm_default_topic(subject, 'Probability spaces')
        self.confirm_default_topic(subject, 'Random variables')

        subject = self.confirm_default_subject('Archaeology and Geography')
        self.confirm_default_topic(subject, 'Prehistoric Archaeology')

        self.confirm_default_topic(subject, 'Historic Archaeology')
        self.confirm_default_topic(subject, 'Forensic Archaeology')
        self.confirm_default_topic(subject, 'Industrial Archaeology')
        self.confirm_default_topic(subject, 'Earth Science')
        self.confirm_default_topic(subject, 'North American Archaeology')
        self.confirm_default_topic(subject, 'Geoarchaeology')
        self.confirm_default_topic(subject, 'Human Evolution')
        self.confirm_default_topic(subject, 'Geographic Information Systems (GIS)')
        self.confirm_default_topic(subject, 'Remote Sensing')

        subject = self.confirm_default_subject('Art Education')
        self.confirm_default_topic(subject, 'Art in Early Childhood I (3 credits)')
        self.confirm_default_topic(subject, 'Art in Early Childhood II (3 credits)')
        self.confirm_default_topic(subject, 'Arts in Recreation (3 credits)')
        self.confirm_default_topic(subject, 'Foundations of Art Education (3 credits)')
        self.confirm_default_topic(subject, 'Practicum: Observation and Analysis of Children’s Learning (3 credits)')
        self.confirm_default_topic(subject, 'Multidisciplinary Approaches to Art and Teaching (3 credits)')
        self.confirm_default_topic(subject, 'Introduction to Community Art Education (3 credits)')
        self.confirm_default_topic(subject, 'Art Education for Adolescents and Adults (3 credits)')
        self.confirm_default_topic(subject, 'Light‑Based Media (3 credits)')
        self.confirm_default_topic(subject, 'Time‑Based Media (3 credits)')
        self.confirm_default_topic(subject, 'Special Topics in Art Education (3 credits)')
        self.confirm_default_topic(subject, 'Art Education for Elementary School (3 credits)')
        self.confirm_default_topic(subject, 'Practicum in the Elementary School (3 credits)')
        self.confirm_default_topic(subject, 'Art Education in the Secondary School I (3 credits)')
        self.confirm_default_topic(subject, 'Practicum in the Secondary School I (3 credits)')
        self.confirm_default_topic(subject, 'Art Education in the Secondary School II (3 credits)')
        self.confirm_default_topic(subject, 'Practicum in the Secondary School II (9 credits)')
        self.confirm_default_topic(subject, 'Community Art Education: Theory and Practice (3 credits)')
        self.confirm_default_topic(subject, 'Professional Practice for Art Educators (3 credits)')
        self.confirm_default_topic(subject, 'Special Topics in Inter‑Related Media and Technologies (3 credits)')


        subject = self.confirm_default_subject('Art History & Museum Studies')
        self.confirm_default_topic(subject, 'Heritage Resource Management')
        self.confirm_default_topic(subject, 'Art Conservation')
        self.confirm_default_topic(subject, 'Archival Studies')
        self.confirm_default_topic(subject, 'Art History')
        self.confirm_default_topic(subject, 'Gallery Design')
        self.confirm_default_topic(subject, 'Native American Art')

        subject = self.confirm_default_subject('Art Studio(BFA)')
        self.confirm_default_topic(subject, 'The role of the artist and audience')
        self.confirm_default_topic(subject, 'The influence of visual culture on social media')
        self.confirm_default_topic(subject, 'The relationship between art and culture')
        self.confirm_default_topic(subject, 'The ethics of cultural appropriation')
        self.confirm_default_topic(subject, 'Health and safety protocols')
        self.confirm_default_topic(subject, 'The social roles of artists and designers')
        self.confirm_default_topic(subject, 'The use of materials, technologies, and processes in art making')
        self.confirm_default_topic(subject, 'The creation of art that reflects personal identity, values, and story')

        subject = self.confirm_default_subject('Biochemistry')

        self.confirm_default_topic(subject, 'Enzymes')
        self.confirm_default_topic(subject, 'Carbohydrates')
        self.confirm_default_topic(subject, 'Cell biology')
        self.confirm_default_topic(subject, 'Enzymology')
        self.confirm_default_topic(subject, 'Metabolism')
        self.confirm_default_topic(subject, 'Amino acids')
        self.confirm_default_topic(subject, 'Applied Biochemistry')
        self.confirm_default_topic(subject, 'Biological membranes')
        self.confirm_default_topic(subject, 'Dna replication repair recombination')
        self.confirm_default_topic(subject, 'Enzyme kinetics')
        self.confirm_default_topic(subject, 'Biotechnology')
        self.confirm_default_topic(subject, 'Chemical metabolism')
        self.confirm_default_topic(subject, 'Lipid metabolism')
        self.confirm_default_topic(subject, 'Microbiology')
        self.confirm_default_topic(subject, 'Molecular Physiology')
        self.confirm_default_topic(subject, 'Biochemical techniques and methods')
        self.confirm_default_topic(subject, 'Cell structure in living organisms')
        self.confirm_default_topic(subject, 'Designing anti-tumor agents')
        self.confirm_default_topic(subject, 'DNA and RNA')
        self.confirm_default_topic(subject, 'Gene expression')
        self.confirm_default_topic(subject, 'Genetics')
        self.confirm_default_topic(subject, 'Lipids')
        self.confirm_default_topic(subject, 'Membrane transport')
        self.confirm_default_topic(subject, 'Nucleic acids')


        subject = self.confirm_default_subject('Biological Sciences')
        self.confirm_default_topic(subject, 'Cell structure and function')
        self.confirm_default_topic(subject, 'Cell division (mitosis, meiosis)')
        self.confirm_default_topic(subject, 'Membrane transport')
        self.confirm_default_topic(subject, 'Cellular respiration')
        self.confirm_default_topic(subject, 'Protein synthesis')
        self.confirm_default_topic(subject, 'Signal transduction')
        self.confirm_default_topic(subject, 'Molecular Level:')
        self.confirm_default_topic(subject, 'DNA structure and replication')
        self.confirm_default_topic(subject, 'Gene expression (transcription, translation)')
        self.confirm_default_topic(subject, 'Genetics (inheritance patterns, mutations)')
        self.confirm_default_topic(subject, 'Genomics (genome sequencing, analysis)')
        self.confirm_default_topic(subject, 'Protein structure and function')
        self.confirm_default_topic(subject, 'Animal physiology (nervous system, circulatory system, endocrine system)')
        self.confirm_default_topic(subject, 'Plant physiology (photosynthesis, transpiration)')
        self.confirm_default_topic(subject, 'Development and embryology')
        self.confirm_default_topic(subject, 'Microbiology (bacterial structure, viral replication)')
        self.confirm_default_topic(subject, 'Population dynamics')
        self.confirm_default_topic(subject, 'Community ecology')
        self.confirm_default_topic(subject, 'Ecosystem function')
        self.confirm_default_topic(subject, 'Biodiversity and conservation')
        self.confirm_default_topic(subject, 'Environmental impacts')
        self.confirm_default_topic(subject, 'Immunology (immune system response)')
        self.confirm_default_topic(subject, 'Neurobiology (brain function, neural pathways)')
        self.confirm_default_topic(subject, 'Marine biology')
        self.confirm_default_topic(subject, 'Evolutionary biology (adaptation, natural selection)')
        self.confirm_default_topic(subject, 'Biotechnology (genetic engineering, gene therapy)')

        subject = self.confirm_default_subject('Business & Supply Chain')

        self.confirm_default_topic(subject, 'The supply chain concept and its components')
        self.confirm_default_topic(subject, 'Value chain analysis')
        self.confirm_default_topic(subject, 'Supply chain planning and forecasting')
        self.confirm_default_topic(subject, 'SCOR Model (Plan, Source, Make, Deliver)')
        self.confirm_default_topic(subject, 'Vendor selection and evaluation')
        self.confirm_default_topic(subject, 'Contract negotiation and management')
        self.confirm_default_topic(subject, 'Supplier relationship management')
        self.confirm_default_topic(subject, 'Strategic sourcing strategies')
        self.confirm_default_topic(subject, 'Transportation modes (road, air, sea)')
        self.confirm_default_topic(subject, 'Warehouse management and inventory control')
        self.confirm_default_topic(subject, 'Distribution network design')
        self.confirm_default_topic(subject, 'Freight forwarding and customs compliance')
        self.confirm_default_topic(subject, 'Inventory forecasting and planning')
        self.confirm_default_topic(subject, 'Inventory optimization techniques (EOQ, JIT)')
        self.confirm_default_topic(subject, 'Inventory control systems')
        self.confirm_default_topic(subject, 'Production planning and scheduling')
        self.confirm_default_topic(subject, 'Quality control and assurance')
        self.confirm_default_topic(subject, 'Lean manufacturing principles')
        self.confirm_default_topic(subject, 'Data analysis and reporting')
        self.confirm_default_topic(subject, 'Predictive modeling and forecasting')
        self.confirm_default_topic(subject, 'Business intelligence tools for supply chain decision making')
        self.confirm_default_topic(subject, 'Environmental impact assessment')
        self.confirm_default_topic(subject, 'Ethical sourcing and labor practices')
        self.confirm_default_topic(subject, 'Sustainable packaging and waste reduction')
        self.confirm_default_topic(subject, 'Identifying potential disruptions')
        self.confirm_default_topic(subject, 'Contingency planning and mitigation strategies')
        self.confirm_default_topic(subject, 'Supply chain resilience building')
        self.confirm_default_topic(subject, 'Network optimization models')
        self.confirm_default_topic(subject, 'Cost reduction strategies')
        self.confirm_default_topic(subject, 'Performance metrics and KPIs')

        subject = self.confirm_default_subject('Management')

        self.confirm_default_topic(subject, 'Conflict resolution')
        self.confirm_default_topic(subject, 'Emotional intelligence')
        self.confirm_default_topic(subject, 'Communication skills')
        self.confirm_default_topic(subject, 'Time management')
        self.confirm_default_topic(subject, 'Change management')
        self.confirm_default_topic(subject, 'Coaching')
        self.confirm_default_topic(subject, 'Problem solving')
        self.confirm_default_topic(subject, 'Communication')
        self.confirm_default_topic(subject, 'Diversity and inclusion')
        self.confirm_default_topic(subject, 'Leadership')
        self.confirm_default_topic(subject, 'Cybersecurity')
        self.confirm_default_topic(subject, 'Presentation skills')
        self.confirm_default_topic(subject, 'Regulatory compliance')
        self.confirm_default_topic(subject, 'Delegation')
        self.confirm_default_topic(subject, 'Feedback')
        self.confirm_default_topic(subject, 'Project management')
        self.confirm_default_topic(subject, 'Stress management')
        self.confirm_default_topic(subject, 'Virtual leadership')
        self.confirm_default_topic(subject, 'Building trust')
        self.confirm_default_topic(subject, 'Customer service')
        self.confirm_default_topic(subject, 'Performance management')
        self.confirm_default_topic(subject, 'Thinking Strategically')
        self.confirm_default_topic(subject, 'Motivating employees')
        self.confirm_default_topic(subject, 'Delegating tasks')

        subject = self.confirm_default_subject('Chemistry')
        self.confirm_default_topic(subject, 'Atomic Structure')
        self.confirm_default_topic(subject, 'Bonding')
        self.confirm_default_topic(subject, 'Electrochemistry')
        self.confirm_default_topic(subject, 'Acid')
        self.confirm_default_topic(subject, 'Stoichiometry')
        self.confirm_default_topic(subject, 'Thermodynamics')
        self.confirm_default_topic(subject, 'Chemical equilibrium')
        self.confirm_default_topic(subject, 'Kinetics')
        self.confirm_default_topic(subject, 'Organic chemistry')
        self.confirm_default_topic(subject, 'Ionic bonding')
        self.confirm_default_topic(subject, 'Nuclear chemistry')
        self.confirm_default_topic(subject, 'Periodic trends')
        self.confirm_default_topic(subject, 'Biochemistry')
        self.confirm_default_topic(subject, 'Composition of mixtures')
        self.confirm_default_topic(subject, 'Inorganic chemistry')
        self.confirm_default_topic(subject, 'IUPAC nomenclature')
        self.confirm_default_topic(subject, 'Making Molecules: Lewis Structures and Molecular Geometries')
        self.confirm_default_topic(subject, 'Chemical reactions')
        self.confirm_default_topic(subject, 'Chemical kinetics')
        self.confirm_default_topic(subject, 'Gases')
        self.confirm_default_topic(subject, 'Reaction types')
        self.confirm_default_topic(subject, 'Bonding and intermolecular forces')
        self.confirm_default_topic(subject, 'Chemical changes')
        self.confirm_default_topic(subject, 'Chemical equations')


        subject = self.confirm_default_subject('Computer Science')
        self.confirm_default_topic(subject, 'Operating Systems')
        self.confirm_default_topic(subject, 'Data structure')
        self.confirm_default_topic(subject, 'Databases')
        self.confirm_default_topic(subject, 'Artificial intelligence')
        self.confirm_default_topic(subject, 'Computer architecture')
        self.confirm_default_topic(subject, 'Programming')
        self.confirm_default_topic(subject, 'Software engineering')
        self.confirm_default_topic(subject, 'Algorithms')
        self.confirm_default_topic(subject, 'Compilers')
        self.confirm_default_topic(subject, 'Web development')
        self.confirm_default_topic(subject, 'Computer graphics')
        self.confirm_default_topic(subject, 'Computer Organization')
        self.confirm_default_topic(subject, 'Analysis of algorithms')
        self.confirm_default_topic(subject, 'Discrete mathematics')
        self.confirm_default_topic(subject, 'Programming Languages')
        self.confirm_default_topic(subject, 'Assembly language programming')
        self.confirm_default_topic(subject, 'Big data')
        self.confirm_default_topic(subject, 'Computational science')
        self.confirm_default_topic(subject, 'Cybersecurity')
        self.confirm_default_topic(subject, 'Distributed computing')
        self.confirm_default_topic(subject, 'Human–computer interaction')
        self.confirm_default_topic(subject, 'Network security')
        self.confirm_default_topic(subject, 'Computer networking')


        subject = self.confirm_default_subject('Dentistry')
        self.confirm_default_topic(subject, 'Oral anatomy and histology')
        self.confirm_default_topic(subject, 'Microbiology')
        self.confirm_default_topic(subject, 'Human physiology')
        self.confirm_default_topic(subject, 'Pathology')
        self.confirm_default_topic(subject, 'Embryology')
        self.confirm_default_topic(subject, 'Filling cavities, tooth repair')
        self.confirm_default_topic(subject, 'Gum disease diagnosis and treatment')
        self.confirm_default_topic(subject, 'Root canal therapy')
        self.confirm_default_topic(subject, 'Alignment of teeth and jaw correction')
        self.confirm_default_topic(subject, 'Replacement of missing teeth with dentures or implants')
        self.confirm_default_topic(subject, 'Surgical procedures in the mouth and jaw')
        self.confirm_default_topic(subject, 'Understanding properties of different dental materials')
        self.confirm_default_topic(subject, 'Anesthesia techniques')
        self.confirm_default_topic(subject, 'Interpreting dental X-rays')
        self.confirm_default_topic(subject, 'Diagnosis and management of oral mucosal diseases')
        self.confirm_default_topic(subject, 'Sterilization procedures and protocols')
        self.confirm_default_topic(subject, 'Building rapport with patients, informed consent, and ethical practice')
 

        subject = self.confirm_default_subject('Digital Audio Arts')
        self.confirm_default_topic(subject, 'Music recording')
        self.confirm_default_topic(subject, 'Recording')
        self.confirm_default_topic(subject, 'Editing')
        self.confirm_default_topic(subject, 'Production')
        self.confirm_default_topic(subject, 'Professional development')
        self.confirm_default_topic(subject, 'Sound design')
        self.confirm_default_topic(subject, 'Media and games')
        self.confirm_default_topic(subject, 'Live events')
        self.confirm_default_topic(subject, 'Broadcasting')
        self.confirm_default_topic(subject, 'Music theory')
        self.confirm_default_topic(subject, 'Sound synthesis')
        self.confirm_default_topic(subject, 'Film study')
        self.confirm_default_topic(subject, 'Digital audio')
        self.confirm_default_topic(subject, 'Digital audio production')

        subject = self.confirm_default_subject('Drama - Performance')

        self.confirm_default_topic(subject, 'Character Analysis')
        self.confirm_default_topic(subject, 'Vocal Techniques')
        self.confirm_default_topic(subject, 'Physicality')
        self.confirm_default_topic(subject, 'Emotional Expression')
        self.confirm_default_topic(subject, 'Improvisation')
        self.confirm_default_topic(subject, 'Stage Presence')
        self.confirm_default_topic(subject, 'Scene Study')
        self.confirm_default_topic(subject, 'Ensemble Work')
        self.confirm_default_topic(subject, 'Creative Development')
        self.confirm_default_topic(subject, 'Devised Theatre')
        self.confirm_default_topic(subject, 'Script Analysis')
        self.confirm_default_topic(subject, 'Playwrighting')
        self.confirm_default_topic(subject, 'Blocking')
        self.confirm_default_topic(subject, 'Pacing')
        self.confirm_default_topic(subject, 'Stagecraft')
        self.confirm_default_topic(subject, 'Warm-up Techniques')
        self.confirm_default_topic(subject, 'Feedback and Evaluation')
        self.confirm_default_topic(subject, 'Character Exploration')
        self.confirm_default_topic(subject, 'Adapting to Different Genres')
        self.confirm_default_topic(subject, 'Scene Study')
        self.confirm_default_topic(subject, 'Devised Theatre')
        self.confirm_default_topic(subject, 'Script Analysis')
        self.confirm_default_topic(subject, 'Playwrighting')
        self.confirm_default_topic(subject, 'Technical Aspects')
        self.confirm_default_topic(subject, 'Blocking')
        self.confirm_default_topic(subject, 'Pacing')
        self.confirm_default_topic(subject, 'Stagecraft')
        self.confirm_default_topic(subject, 'Important Considerations')
        self.confirm_default_topic(subject, 'Warm-up Techniques')
        self.confirm_default_topic(subject, 'Feedback and Evaluation')
        self.confirm_default_topic(subject, 'Character Exploration')
        self.confirm_default_topic(subject, 'Adapting to Different Genres')

        subject = self.confirm_default_subject('Drama Education')
        self.confirm_default_topic(subject, 'Verbal and nonverbal communication')
        self.confirm_default_topic(subject, 'Expressing emotions')
        self.confirm_default_topic(subject, 'Creativity')
        self.confirm_default_topic(subject, 'Imagination')
        self.confirm_default_topic(subject, 'Storytelling')
        self.confirm_default_topic(subject, 'Empathy')
        self.confirm_default_topic(subject, 'Understanding characters')
        self.confirm_default_topic(subject, 'Relating to others')
        self.confirm_default_topic(subject, 'Problem solving')
        self.confirm_default_topic(subject, 'Social skills')
        self.confirm_default_topic(subject, 'Teamwork and leadership')
        self.confirm_default_topic(subject, 'Listening and responding')
        self.confirm_default_topic(subject, 'Critical thinking')
        self.confirm_default_topic(subject, 'Time management')
        self.confirm_default_topic(subject, 'Research')

        subject = self.confirm_default_subject('Dramatic Arts')

        self.confirm_default_topic(subject, 'Acting')
        self.confirm_default_topic(subject, 'Playwriting')
        self.confirm_default_topic(subject, 'Directing')
        self.confirm_default_topic(subject, 'Character development')
        self.confirm_default_topic(subject, 'Movement')
        self.confirm_default_topic(subject, 'Voice training')
        self.confirm_default_topic(subject, 'Dramatic theory')
        self.confirm_default_topic(subject, 'Design')
        self.confirm_default_topic(subject, 'Contemporary theater')
        self.confirm_default_topic(subject, 'Script interpretation')
        self.confirm_default_topic(subject, 'Rehearsing')
        self.confirm_default_topic(subject, 'Audience response')

        subject = self.confirm_default_subject('Economics')

        self.confirm_default_topic(subject, 'Labor Economics')
        self.confirm_default_topic(subject, 'International Economics')
        self.confirm_default_topic(subject, 'Macroeconomics')
        self.confirm_default_topic(subject, 'Microeconomics')
        self.confirm_default_topic(subject, 'Development Economics')
        self.confirm_default_topic(subject, 'Environmental economics')
        self.confirm_default_topic(subject, 'Financial economics')
        self.confirm_default_topic(subject, 'Health economics')
        self.confirm_default_topic(subject, 'Industrial organization')
        self.confirm_default_topic(subject, 'Market structures')
        self.confirm_default_topic(subject, 'Public economics')
        self.confirm_default_topic(subject, 'Behavioral economics')
        self.confirm_default_topic(subject, 'Demand and supply')
        self.confirm_default_topic(subject, 'History')
        self.confirm_default_topic(subject, 'Interdisciplinary economics')
        self.confirm_default_topic(subject, 'International trade')


        subject = self.confirm_default_subject('Engineering')

        self.confirm_default_topic(subject, 'Fluid mechanics')
        self.confirm_default_topic(subject, 'Automation and robotics')
        self.confirm_default_topic(subject, 'Heat transfer')
        self.confirm_default_topic(subject, 'Project management')
        self.confirm_default_topic(subject, 'Thermodynamics')
        self.confirm_default_topic(subject, 'Additive manufacturing material properties')
        self.confirm_default_topic(subject, 'AI and civil engineering')
        self.confirm_default_topic(subject, 'Computational fluid dynamics')
        self.confirm_default_topic(subject, 'Control system')
        self.confirm_default_topic(subject, 'Electrical machines')
        self.confirm_default_topic(subject, 'Energy')
        self.confirm_default_topic(subject, 'Finite element method')
        self.confirm_default_topic(subject, 'Industrial')
        self.confirm_default_topic(subject, 'Magnetism')
        self.confirm_default_topic(subject, 'Materials')
        self.confirm_default_topic(subject, 'Mechanical')

        subject = self.confirm_default_subject('English')
        self.confirm_default_topic(subject, 'Greetings and introductions')
        self.confirm_default_topic(subject, 'Asking and answering simple questions')
        self.confirm_default_topic(subject, 'Basic vocabulary for daily life')
        self.confirm_default_topic(subject, 'Name, age, nationality')
        self.confirm_default_topic(subject, 'Family members')
        self.confirm_default_topic(subject, 'Where you live')
        self.confirm_default_topic(subject, 'Waking up, eating meals')
        self.confirm_default_topic(subject, 'Work/study schedule')
        self.confirm_default_topic(subject, 'Hobbies and leisure activities')
        self.confirm_default_topic(subject, 'Weather')
        self.confirm_default_topic(subject, 'Food and dining')
        self.confirm_default_topic(subject, 'Travel plans')
        self.confirm_default_topic(subject, 'Current events')
        self.confirm_default_topic(subject, 'Subject-verb agreement')
        self.confirm_default_topic(subject, 'Verb tenses')
        self.confirm_default_topic(subject, 'Pronouns')
        self.confirm_default_topic(subject, 'Articles')
        self.confirm_default_topic(subject, 'Prepositions')
        self.confirm_default_topic(subject, 'Listening comprehension')
        self.confirm_default_topic(subject, 'Speaking fluency')
        self.confirm_default_topic(subject, 'Reading comprehension')
        self.confirm_default_topic(subject, 'Writing skills')

        subject = self.confirm_default_subject('Education')

        self.confirm_default_topic(subject, 'Literacy development')
        self.confirm_default_topic(subject, 'Reading comprehension')
        self.confirm_default_topic(subject, 'writing skills')
        self.confirm_default_topic(subject, 'vocabulary building')
        self.confirm_default_topic(subject, 'phonics instruction')
        self.confirm_default_topic(subject, 'Social-emotional learning (SEL)')
        self.confirm_default_topic(subject, 'Emotional regulation')
        self.confirm_default_topic(subject, 'empathy')
        self.confirm_default_topic(subject, 'conflict resolution')
        self.confirm_default_topic(subject, 'social awareness')
        self.confirm_default_topic(subject, 'Educational technology')
        self.confirm_default_topic(subject, 'Integrating digital tools')
        self.confirm_default_topic(subject, 'online learning platforms')
        self.confirm_default_topic(subject, 'digital literacy')
        self.confirm_default_topic(subject, 'Classroom management')
        self.confirm_default_topic(subject, 'Creating a positive learning environment')
        self.confirm_default_topic(subject, 'student engagement strategies')
        self.confirm_default_topic(subject, 'behavior management')
        self.confirm_default_topic(subject, 'Curriculum design')
        self.confirm_default_topic(subject, 'Developing aligned learning objectives')
        self.confirm_default_topic(subject, 'lesson planning')
        self.confirm_default_topic(subject, 'assessment strategies')
        self.confirm_default_topic(subject, 'Differentiated instruction')
        self.confirm_default_topic(subject,
                                   'Tailoring teaching methods to cater to diverse student needs and learning styles')
        self.confirm_default_topic(subject, 'Assessment practices')
        self.confirm_default_topic(subject, 'Formative and summative assessments')
        self.confirm_default_topic(subject, 'standardized testing')
        self.confirm_default_topic(subject, 'performance-based assessments')
        self.confirm_default_topic(subject, 'Blended learning')
        self.confirm_default_topic(subject,
                                   'Combining traditional face-to-face instruction with online learning components')
        self.confirm_default_topic(subject, 'Gamification')
        self.confirm_default_topic(subject, 'Incorporating game-like elements to enhance engagement and motivation')
        self.confirm_default_topic(subject, 'Critical thinking skills')
        self.confirm_default_topic(subject, 'Analyzing information')
        self.confirm_default_topic(subject, 'problem-solving')
        self.confirm_default_topic(subject, 'evaluating evidence')
        self.confirm_default_topic(subject, 'Impact of technology on learning')
        self.confirm_default_topic(subject, 'Examining the benefits and challenges of technology in the classroom')
        self.confirm_default_topic(subject, 'Teacher effectiveness')
        self.confirm_default_topic(subject, 'Professional development')
        self.confirm_default_topic(subject, 'instructional practices')
        self.confirm_default_topic(subject, 'teacher collaboration')
        self.confirm_default_topic(subject, 'Addressing learning poverty')

        subject = self.confirm_default_subject('Environmental Science')
        self.confirm_default_topic(subject, 'Ecology')
        self.confirm_default_topic(subject, 'Atmospheric Science')
        self.confirm_default_topic(subject, 'Hydrology')
        self.confirm_default_topic(subject, 'Geoscience')
        self.confirm_default_topic(subject, 'Environmental Chemistry')
        self.confirm_default_topic(subject, 'Biodiversity')
        self.confirm_default_topic(subject, 'Renewable Energy')
        self.confirm_default_topic(subject, 'Environmental Policy and Law')
        self.confirm_default_topic(subject, 'Sustainability')
        self.confirm_default_topic(subject, 'Specific learning topics within these areas might include')
        self.confirm_default_topic(subject, 'Climate Change')
        self.confirm_default_topic(subject, 'Pollution Control')
        self.confirm_default_topic(subject, 'Land Use Planning')
        self.confirm_default_topic(subject, 'Environmental Impact Assessment')
        self.confirm_default_topic(subject, 'Environmental Monitoring')
        self.confirm_default_topic(subject, 'Conservation Biology')
        self.confirm_default_topic(subject, 'Environmental Justice')


        subject = self.confirm_default_subject('Finance')
        self.confirm_default_topic(subject, 'Credit')
        self.confirm_default_topic(subject, 'Debt')
        self.confirm_default_topic(subject, 'Investing')
        self.confirm_default_topic(subject, 'Retirement')
        self.confirm_default_topic(subject, 'Saving')
        self.confirm_default_topic(subject, 'Banking')
        self.confirm_default_topic(subject, 'Income tax')
        self.confirm_default_topic(subject, 'Insurance')
        self.confirm_default_topic(subject, 'Financial basics everyone should know')
        self.confirm_default_topic(subject, 'Loans')
        self.confirm_default_topic(subject, 'Alternative investments')
        self.confirm_default_topic(subject, 'Corporate finance')
        self.confirm_default_topic(subject, 'Credit scores')
        self.confirm_default_topic(subject, 'Earning')
        self.confirm_default_topic(subject, 'Investment fraud prevention')
        self.confirm_default_topic(subject, 'Managing cash flow')
        self.confirm_default_topic(subject, 'Managing your personal finances')
        self.confirm_default_topic(subject, 'Risk management')
        self.confirm_default_topic(subject, 'Accounting')
        self.confirm_default_topic(subject, 'Asset management')
        self.confirm_default_topic(subject, 'Banking and financial institutions')
        self.confirm_default_topic(subject, 'Budgeting')
        self.confirm_default_topic(subject, 'Balancing bank accounts')
        self.confirm_default_topic(subject, 'Borrowing')

        subject = self.confirm_default_subject('Humanities')
        self.confirm_default_topic(subject, 'Art')
        self.confirm_default_topic(subject, 'Communication')
        self.confirm_default_topic(subject, 'History')
        self.confirm_default_topic(subject, 'Literature')
        self.confirm_default_topic(subject, 'Philosophy')
        self.confirm_default_topic(subject, 'Religion')
        self.confirm_default_topic(subject, 'Politics')
        self.confirm_default_topic(subject, 'Cultural studies')
        self.confirm_default_topic(subject, 'History and anthropology')
        self.confirm_default_topic(subject, 'Human')
        self.confirm_default_topic(subject, 'Law')
        self.confirm_default_topic(subject, 'Psychology')
        self.confirm_default_topic(subject, 'Public Administration')

        subject = self.confirm_default_subject('Social Sciences')

        self.confirm_default_topic(subject, 'Economics')
        self.confirm_default_topic(subject, 'Political science')
        self.confirm_default_topic(subject, 'Anthropology')
        self.confirm_default_topic(subject, 'Psychology')
        self.confirm_default_topic(subject, 'Sociology')
        self.confirm_default_topic(subject, 'Geography')
        self.confirm_default_topic(subject, 'Social work')
        self.confirm_default_topic(subject, 'Cultural assimilation')
        self.confirm_default_topic(subject, 'Culture')
        self.confirm_default_topic(subject, 'Education')
        self.confirm_default_topic(subject, 'Government')
        self.confirm_default_topic(subject, 'History')
        self.confirm_default_topic(subject, 'Law')
        self.confirm_default_topic(subject, 'Linguistics')
        self.confirm_default_topic(subject, 'Public policy')
        self.confirm_default_topic(subject, 'Aging')

        subject = self.confirm_default_subject('Geography')
        self.confirm_default_topic(subject, 'Landforms')
        self.confirm_default_topic(subject, 'Climatology')
        self.confirm_default_topic(subject, 'Hydrology')
        self.confirm_default_topic(subject, 'Geomorphology')
        self.confirm_default_topic(subject, 'Biogeography')
        self.confirm_default_topic(subject, 'Human Geography')
        self.confirm_default_topic(subject, 'Population Geography')
        self.confirm_default_topic(subject, 'Cultural Geography')
        self.confirm_default_topic(subject, 'Economic Geography')
        self.confirm_default_topic(subject, 'Political Geography')
        self.confirm_default_topic(subject, 'Urban Geography')
        self.confirm_default_topic(subject, 'Geographical Skills')
        self.confirm_default_topic(subject, 'Map reading and interpretation')
        self.confirm_default_topic(subject, 'Data analysis and visualization')
        self.confirm_default_topic(subject, 'Geographic Information Systems (GIS)')
        self.confirm_default_topic(subject, 'Fieldwork techniques')
        self.confirm_default_topic(subject, 'Key Concepts in Geography')
        self.confirm_default_topic(subject, 'Place')
        self.confirm_default_topic(subject, 'Space')
        self.confirm_default_topic(subject, 'Scale')
        self.confirm_default_topic(subject, 'Interconnection')
        self.confirm_default_topic(subject, 'Sustainability')
        subject = self.confirm_default_subject('History')
        self.confirm_default_topic(subject, 'Ancient History (e.g., Mesopotamia, Egypt, Greece, Rome)')
        self.confirm_default_topic(subject, 'Medieval History (e.g., European Middle Ages)')
        self.confirm_default_topic(subject, 'Early Modern History (e.g., Renaissance, Age of Exploration)')
        self.confirm_default_topic(subject, 'Modern History (e.g., Industrial Revolution, World Wars)')
        self.confirm_default_topic(subject, 'Major Themes')
        self.confirm_default_topic(subject, 'Political History')
        self.confirm_default_topic(subject, 'Social History')
        self.confirm_default_topic(subject, 'Economic History')
        self.confirm_default_topic(subject, 'Cultural History')
        self.confirm_default_topic(subject, 'Military History')
        self.confirm_default_topic(subject, 'Specific Topics')
        self.confirm_default_topic(subject, 'The Holocaust')
        self.confirm_default_topic(subject, 'The French Revolution')
        self.confirm_default_topic(subject, 'The Civil Rights Movement')
        self.confirm_default_topic(subject, 'The Cold War')
        self.confirm_default_topic(subject, 'The Industrial Revolution')
        self.confirm_default_topic(subject, 'The impact of colonialism')
        self.confirm_default_topic(subject, "Women's history")
        self.confirm_default_topic(subject, 'Global health issues throughout history')
        self.confirm_default_topic(subject, 'Important Historical Skills to Develop')
        self.confirm_default_topic(subject, 'Critical Thinking')
        self.confirm_default_topic(subject, 'Historical Context')
        self.confirm_default_topic(subject, 'Cause and Effect Analysis')
        self.confirm_default_topic(subject, 'Comparison and Contrast')
        self.confirm_default_topic(subject, 'Historical Interpretation')

        subject = self.confirm_default_subject('Human Resource')

        self.confirm_default_topic(subject, 'Compensation')
        self.confirm_default_topic(subject, 'Recruitment and selection')
        self.confirm_default_topic(subject, 'Training and development')
        self.confirm_default_topic(subject, 'Ethics for hr')
        self.confirm_default_topic(subject, 'Inclusion and diversity')
        self.confirm_default_topic(subject, 'Occupational safety and health')
        self.confirm_default_topic(subject, 'Labor relations')
        self.confirm_default_topic(subject, 'Organizational behavior')
        self.confirm_default_topic(subject, 'Performance management')
        self.confirm_default_topic(subject, 'Learning and development')
        self.confirm_default_topic(subject, 'Talent acquisition')
        self.confirm_default_topic(subject, 'HR planning')
        self.confirm_default_topic(subject, 'Strategic workforce planning')
        self.confirm_default_topic(subject, 'Business communication')
        self.confirm_default_topic(subject, 'Communication')
        self.confirm_default_topic(subject, 'HR administration')
        self.confirm_default_topic(subject, 'HR metrics and Dashboarding')
        self.confirm_default_topic(subject, 'Change management')
        self.confirm_default_topic(subject, 'Organization')
        self.confirm_default_topic(subject, 'Organizational alignment')
        self.confirm_default_topic(subject, 'Recruitment analytics')
        self.confirm_default_topic(subject, 'Succession planning')
        self.confirm_default_topic(subject, 'Virtual teams')
        self.confirm_default_topic(subject, 'Career planning')

        subject = self.confirm_default_subject('Management & Labour Relations')
        self.confirm_default_topic(subject, 'Employment Standards Legislation')
        self.confirm_default_topic(subject, 'Labour Relations Acts')
        self.confirm_default_topic(subject, 'Case Law related to employment and labour relations')
        self.confirm_default_topic(subject, 'Certification process')
        self.confirm_default_topic(subject, 'Bargaining unit determination')
        self.confirm_default_topic(subject, 'Negotiation strategies and tactics')
        self.confirm_default_topic(subject, 'Collective agreement content (wages, hours, working conditions)')
        self.confirm_default_topic(subject, 'Grievance procedure')
        self.confirm_default_topic(subject, 'Investigation process')
        self.confirm_default_topic(subject, 'Arbitration process')
        self.confirm_default_topic(subject, 'Conciliation')
        self.confirm_default_topic(subject, 'Mediation')
        self.confirm_default_topic(subject, 'Strikes and lockouts')
        self.confirm_default_topic(subject, 'Performance management')
        self.confirm_default_topic(subject, 'Disciplinary action')
        self.confirm_default_topic(subject, 'Workplace harassment and discrimination')
        self.confirm_default_topic(subject, 'Employee engagement strategies')
        self.confirm_default_topic(subject, 'Leadership in a unionized environment')
        self.confirm_default_topic(subject, 'Labour relations strategy development')
        self.confirm_default_topic(subject, 'Managing change in a unionized workplace')
        self.confirm_default_topic(subject, 'Globalization and its impact on labour relations')
        self.confirm_default_topic(subject, 'Technology and the changing nature of work')
        self.confirm_default_topic(subject, 'Diversity and inclusion in the workplace')
        self.confirm_default_topic(subject, 'Workplace mental health')

        subject = self.confirm_default_subject('Indigenous Art')

        self.confirm_default_topic(subject, 'Cultural context')
        self.confirm_default_topic(subject, 'Storytelling')
        self.confirm_default_topic(subject, 'Connection to nature')
        self.confirm_default_topic(subject, 'Symbolism')
        self.confirm_default_topic(subject, 'Diversity of styles')
        self.confirm_default_topic(subject, 'Spiritual and ritualistic aspects')
        self.confirm_default_topic(subject, 'Traditional and contemporary art')

        subject = self.confirm_default_subject('Indigenous Education')

        self.confirm_default_topic(subject, 'Indigenous knowledge')
        self.confirm_default_topic(subject, 'Indigenous worldviews')
        self.confirm_default_topic(subject, 'Indigenous identities')
        self.confirm_default_topic(subject, 'Indigenous history')
        self.confirm_default_topic(subject, 'Indigenous traditions')

        subject = self.confirm_default_subject('Indigenous Governance and Business')
        self.confirm_default_topic(subject, 'Indigenous Legal Systems')
        self.confirm_default_topic(subject, 'Indian Act and its Impact')
        self.confirm_default_topic(subject, 'Self-Government Agreements')
        self.confirm_default_topic(subject, 'Indigenous Business Development')
        self.confirm_default_topic(subject, 'Natural Resource Management')
        self.confirm_default_topic(subject, 'Indigenous Negotiations')
        self.confirm_default_topic(subject, 'Indigenous Leadership')
        self.confirm_default_topic(subject, 'Community Engagement')
        self.confirm_default_topic(subject, 'Indigenous Economics')
        self.confirm_default_topic(subject, 'Indigenous Knowledge Systems')
        self.confirm_default_topic(subject, 'Decolonization and Reconciliation')

        subject = self.confirm_default_subject('Management Indigenous Health')

        self.confirm_default_topic(subject, 'Indigenous Health Disparities')
        self.confirm_default_topic(subject, 'Cultural Safety and Competency')
        self.confirm_default_topic(subject, 'Indigenous Knowledge Systems')
        self.confirm_default_topic(subject, 'Community Engagement and Collaboration')
        self.confirm_default_topic(subject, 'Policy and Advocacy')
        self.confirm_default_topic(subject, 'Research Ethics with Indigenous Communities')

        subject = self.confirm_default_subject('Indigenous Studies International')

        self.confirm_default_topic(subject, 'Indigenous histories and colonization')
        self.confirm_default_topic(subject, 'Traditional ecological knowledge (TEK)')
        self.confirm_default_topic(subject, 'Indigenous languages and literatures')
        self.confirm_default_topic(subject, 'Indigenous governance and self-determination')
        self.confirm_default_topic(subject, 'Indigenous health and wellness')
        self.confirm_default_topic(subject, 'Indigenous art and cultural expression')
        self.confirm_default_topic(subject, 'Indigenous rights and activism')
        self.confirm_default_topic(subject, 'Comparative Indigenous studies')
        self.confirm_default_topic(subject, 'Decolonization and Indigenous methodologies')
        self.confirm_default_topic(subject, 'Indigenous perspectives on environmental issues')

        subject = self.confirm_default_subject('Kinesiology')
        self.confirm_default_topic(subject, 'Anatomy and Physiology')
        self.confirm_default_topic(subject, 'Biomechanics')
        self.confirm_default_topic(subject, 'Exercise Physiology')
        self.confirm_default_topic(subject, 'Motor Control')
        self.confirm_default_topic(subject, 'Sport Psychology')
        self.confirm_default_topic(subject, 'Sports Medicine')
        self.confirm_default_topic(subject, 'Fitness Assessment and Training')
        self.confirm_default_topic(subject, 'Nutrition for Exercise')
        self.confirm_default_topic(subject, 'Growth and Development')
        self.confirm_default_topic(subject, 'Health Promotion and Physical Activity')

        subject = self.confirm_default_subject('Law')

        self.confirm_default_topic(subject, 'Criminal law')
        self.confirm_default_topic(subject, 'Property law')
        self.confirm_default_topic(subject, 'Human rights')
        self.confirm_default_topic(subject, 'Immigration law')
        self.confirm_default_topic(subject, 'Constitutional law')
        self.confirm_default_topic(subject, 'Health')
        self.confirm_default_topic(subject, 'Small Claims Court')
        self.confirm_default_topic(subject, 'Wills and powers of attorney')
        self.confirm_default_topic(subject, 'Civil procedure')
        self.confirm_default_topic(subject, 'Contract')
        self.confirm_default_topic(subject, 'Income assistance')
        self.confirm_default_topic(subject, 'Rights')
        self.confirm_default_topic(subject, 'Tort')
        self.confirm_default_topic(subject, 'Abuse and family violence')
        self.confirm_default_topic(subject, 'Education law')
        self.confirm_default_topic(subject, 'Legal actions')


        subject = self.confirm_default_subject('Marketing Mathematics')
        self.confirm_default_topic(subject, 'Descriptive Statistics')
        self.confirm_default_topic(subject, 'Inferential Statistics')
        self.confirm_default_topic(subject, 'Probability')
        self.confirm_default_topic(subject, 'Conversion Rate Calculation')
        self.confirm_default_topic(subject, 'Cost Per Acquisition (CPA)')
        self.confirm_default_topic(subject, 'Return on Investment (ROI)')
        self.confirm_default_topic(subject, 'Break-Even Analysis')
        self.confirm_default_topic(subject, 'Customer Lifetime Value (CLTV)')
        self.confirm_default_topic(subject, 'Market Share Calculation')
        self.confirm_default_topic(subject, 'Regression Analysis')
        self.confirm_default_topic(subject, 'Linear Algebra')
        self.confirm_default_topic(subject, 'Important considerations')
        self.confirm_default_topic(subject, 'Data Collection and Analysis')
        self.confirm_default_topic(subject, 'Marketing Metrics')
        self.confirm_default_topic(subject, 'Application in Decision Making')
        subject = self.confirm_default_subject('Mathematics Education')
        self.confirm_default_topic(subject, 'Mathematical cognition')
        self.confirm_default_topic(subject, 'Teaching strategies')
        self.confirm_default_topic(subject, 'Combinatorics')
        self.confirm_default_topic(subject, 'Attitudes towards mathematics')
        self.confirm_default_topic(subject, 'Learning styles')
        self.confirm_default_topic(subject, 'Realistic mathematics education')
        self.confirm_default_topic(subject, 'Analysis of resilience')
        self.confirm_default_topic(subject, 'Big ideas of math')

        subject = self.confirm_default_subject('Medicine')

        self.confirm_default_topic(subject, 'Human Anatomy')
        self.confirm_default_topic(subject, 'Physiology')
        self.confirm_default_topic(subject, 'Biochemistry')
        self.confirm_default_topic(subject, 'Microbiology')
        self.confirm_default_topic(subject, 'Pathology')
        self.confirm_default_topic(subject, 'Physical Examination')
        self.confirm_default_topic(subject, 'Diagnostic Procedures')
        self.confirm_default_topic(subject, 'Medical History Taking')
        self.confirm_default_topic(subject, 'Patient Communication')
        self.confirm_default_topic(subject, 'Drug Mechanisms')
        self.confirm_default_topic(subject, 'Drug Interactions')
        self.confirm_default_topic(subject, 'Medication Administration')
        self.confirm_default_topic(subject, 'Internal Medicine')
        self.confirm_default_topic(subject, 'Surgery')
        self.confirm_default_topic(subject, 'Pediatrics')
        self.confirm_default_topic(subject, 'Obstetrics and Gynecology')
        self.confirm_default_topic(subject, 'Psychiatry')
        self.confirm_default_topic(subject, 'Neurology')
        self.confirm_default_topic(subject, 'Cardiology')
        self.confirm_default_topic(subject, 'Oncology')
        self.confirm_default_topic(subject, 'Medical Ethics')
        self.confirm_default_topic(subject, 'Public Health')
        self.confirm_default_topic(subject, 'Health Informatics')
        self.confirm_default_topic(subject, 'Medical Research')
        self.confirm_default_topic(subject, 'Interprofessional Education')
        self.confirm_default_topic(subject, 'Artificial Intelligence in Medicine')

        subject = self.confirm_default_subject('Modern Languages Education')

        self.confirm_default_topic(subject, 'Culture')
        self.confirm_default_topic(subject, 'Grammar')
        self.confirm_default_topic(subject, 'Real-life situations')
        self.confirm_default_topic(subject, 'Creative communication')
        self.confirm_default_topic(subject, 'Reinforcing knowledge')
        self.confirm_default_topic(subject, 'Eliciting meaning from text')
        self.confirm_default_topic(subject, 'Language acquisition')
        self.confirm_default_topic(subject, 'Teaching a language')
        self.confirm_default_topic(subject, 'Language status in society')
        self.confirm_default_topic(subject, 'Teaching approaches')
        self.confirm_default_topic(subject, 'Digital technologies')

        subject = self.confirm_default_subject('Music Education')

        self.confirm_default_topic(subject, 'Harmony')
        self.confirm_default_topic(subject, 'Rhythm')
        self.confirm_default_topic(subject, 'Musical notation')
        self.confirm_default_topic(subject, 'African American song')
        self.confirm_default_topic(subject, 'Lullabies')
        self.confirm_default_topic(subject, 'Conducting')
        self.confirm_default_topic(subject, 'Playing instruments')
        self.confirm_default_topic(subject, 'Ensemble participation')
        self.confirm_default_topic(subject, 'Lesson planning')
        self.confirm_default_topic(subject, 'Assessment')
        self.confirm_default_topic(subject, 'Creativity')
        self.confirm_default_topic(subject, 'Inclusive teaching')
        self.confirm_default_topic(subject, 'Kodaly pedagogy')
        self.confirm_default_topic(subject, 'Jazz pedagogy')

        subject = self.confirm_default_subject('Neuroscience')

        self.confirm_default_topic(subject, 'Cognitive neuroscience')
        self.confirm_default_topic(subject, 'Computational neuroscience')
        self.confirm_default_topic(subject, 'Developmental cognitive neuroscience')
        self.confirm_default_topic(subject, 'Affective Neuroscience')
        self.confirm_default_topic(subject, 'Behavioral neuroscience')
        self.confirm_default_topic(subject, 'Cellular Neuroscience')
        self.confirm_default_topic(subject, 'Development of cognitive flexibility')
        self.confirm_default_topic(subject, 'Does hallucination cause any brain deficit')
        self.confirm_default_topic(subject, 'Neurogenetics')
        self.confirm_default_topic(subject, 'Neuroplasticity')

        subject = self.confirm_default_subject('New Media')

        self.confirm_default_topic(subject, 'Media Literacy')
        self.confirm_default_topic(subject, 'Digital Content Creation')
        self.confirm_default_topic(subject, 'Social Media Marketing')
        self.confirm_default_topic(subject, 'Web Design and Development')
        self.confirm_default_topic(subject, 'Interactive Storytelling')
        self.confirm_default_topic(subject, 'Emerging Technologies')

        subject = self.confirm_default_subject('Nursing')

        self.confirm_default_topic(subject, 'Mental health')
        self.confirm_default_topic(subject, 'Patient safety')
        self.confirm_default_topic(subject, 'Burnout prevention strategies for nurses')
        self.confirm_default_topic(subject, 'Pain management')
        self.confirm_default_topic(subject, 'Palliative care')
        self.confirm_default_topic(subject, 'Chronic condition')
        self.confirm_default_topic(subject, 'Health diversity')
        self.confirm_default_topic(subject, 'Nursing education')
        self.confirm_default_topic(subject, 'Nursing management')
        self.confirm_default_topic(subject, 'Pediatric nursing practices')

        subject = self.confirm_default_subject('Philosophy')

        self.confirm_default_topic(subject, 'Ethics')
        self.confirm_default_topic(subject, 'Political philosophy')
        self.confirm_default_topic(subject, 'Philosophy of science')
        self.confirm_default_topic(subject, 'Epistemology')
        self.confirm_default_topic(subject, 'Logic')
        self.confirm_default_topic(subject, 'Metaphysics')
        self.confirm_default_topic(subject, 'Philosophy of mind')
        self.confirm_default_topic(subject, 'Analytic philosophy')
        self.confirm_default_topic(subject, 'Philosophy of language')
        self.confirm_default_topic(subject, 'Continental philosophy')
        self.confirm_default_topic(subject, 'Aesthetics')

        subject = self.confirm_default_subject('Physical Education')

        self.confirm_default_topic(subject, 'Movement skills')
        self.confirm_default_topic(subject, 'Fundamental movement skills')
        self.confirm_default_topic(subject, 'Movement competence')
        self.confirm_default_topic(subject, 'Physical fitness')
        self.confirm_default_topic(subject, 'Healthy living')
        self.confirm_default_topic(subject, 'Active living')
        self.confirm_default_topic(subject, 'Healthy lifestyles practices')
        self.confirm_default_topic(subject, 'Safety behaviors')
        self.confirm_default_topic(subject, 'Outdoor hazard response')
        self.confirm_default_topic(subject, 'Social-emotional learning')
        self.confirm_default_topic(subject, 'Stress coping')
        self.confirm_default_topic(subject, 'Positive motivation')
        self.confirm_default_topic(subject, 'Relationship building')
        self.confirm_default_topic(subject, 'Adapted physical education')

        subject = self.confirm_default_subject('Physics')

        self.confirm_default_topic(subject, 'Classical mechanics')
        self.confirm_default_topic(subject, 'Modern physics')
        self.confirm_default_topic(subject, 'Thermodynamics')
        self.confirm_default_topic(subject, 'Energy')
        self.confirm_default_topic(subject, 'Fluids')
        self.confirm_default_topic(subject, 'General relativity')
        self.confirm_default_topic(subject, 'Optics')
        self.confirm_default_topic(subject, 'Standing waves')
        self.confirm_default_topic(subject, 'Astrophysics')
        self.confirm_default_topic(subject, 'Electricity')
        self.confirm_default_topic(subject, 'Mathematical physics')
        self.confirm_default_topic(subject, 'Mechanics')
        self.confirm_default_topic(subject, 'Quantum mechanics')
        self.confirm_default_topic(subject, 'Electrostatics')
        self.confirm_default_topic(subject, 'Freshman physics')
        self.confirm_default_topic(subject, 'Kinematics')
        self.confirm_default_topic(subject, 'Momentum')
        self.confirm_default_topic(subject, 'Atomic Structure')
        self.confirm_default_topic(subject, 'Condensed matter physics')
        self.confirm_default_topic(subject, 'Classical electromagnetism')
        self.confirm_default_topic(subject, "Newton's first law")
        self.confirm_default_topic(subject, 'Electromagnetism')
        self.confirm_default_topic(subject, 'Electricity and magnetism')
        self.confirm_default_topic(subject, 'Circular motion')

        subject = self.confirm_default_subject('Political Science')

        self.confirm_default_topic(subject, "International relations")
        self.confirm_default_topic(subject, "Comparative politics")
        self.confirm_default_topic(subject, "Political theory")
        self.confirm_default_topic(subject, "Public administration")
        self.confirm_default_topic(subject, "Global politics")
        self.confirm_default_topic(subject, "Modern political analysis")
        self.confirm_default_topic(subject, "Democratic processes")
        self.confirm_default_topic(subject, "International conflict")
        self.confirm_default_topic(subject, "Public opinion")

        subject = self.confirm_default_subject('Psychology')

        self.confirm_default_topic(subject, "Social cognition")
        self.confirm_default_topic(subject, "Social media and the internet")
        self.confirm_default_topic(subject, "Attitudes")
        self.confirm_default_topic(subject, "Behaviorism")
        self.confirm_default_topic(subject, "Eating disorder")
        self.confirm_default_topic(subject, "Health psychology")
        self.confirm_default_topic(subject, "Parenting")
        self.confirm_default_topic(subject, "Schizophrenia")
        self.confirm_default_topic(subject, "Stereotypes and prejudice in society")
        self.confirm_default_topic(subject, "The impact of cyberbullying on self-esteem")
        self.confirm_default_topic(subject, "Aging and older adults")
        self.confirm_default_topic(subject, "Bullying")
        self.confirm_default_topic(subject, "Clinical psychology")
        self.confirm_default_topic(subject, "Cognitive rehabilitation")
        self.confirm_default_topic(subject, "Constructivism")
        self.confirm_default_topic(subject, "Depression")
        self.confirm_default_topic(subject, "Developmental psychology")
        self.confirm_default_topic(subject, "Cognition")
        self.confirm_default_topic(subject, "Leadership")
        self.confirm_default_topic(subject, "Mindfulness")
        self.confirm_default_topic(subject, "Online dating and interpersonal attraction")
        self.confirm_default_topic(subject, "Perception")
        self.confirm_default_topic(subject, "Person perception")
        self.confirm_default_topic(subject, "Personality psychology")

        subject = self.confirm_default_subject('Public Health')

        self.confirm_default_topic(subject, "Epidemiology")
        self.confirm_default_topic(subject, "Biostatistics")
        self.confirm_default_topic(subject, "Environmental Health")
        self.confirm_default_topic(subject, "Health Policy")
        self.confirm_default_topic(subject, "Health Promotion")
        self.confirm_default_topic(subject, "Disease Prevention and Control")
        self.confirm_default_topic(subject, "Community Health Assessment")
        self.confirm_default_topic(subject, "Emergency Preparedness")
        self.confirm_default_topic(subject, "Public Health Ethics")
        self.confirm_default_topic(subject, "Social Determinants of Health")
        self.confirm_default_topic(subject, "Other important topics may include")
        self.confirm_default_topic(subject, "Maternal and Child Health")
        self.confirm_default_topic(subject, "Mental Health Promotion")
        self.confirm_default_topic(subject, "Nutrition and Physical Activity")
        self.confirm_default_topic(subject, "Global Health")
        self.confirm_default_topic(subject, "Health Disparities")

        subject = self.confirm_default_subject('Religious Studies')

        self.confirm_default_topic(subject, "Major World Religions")
        self.confirm_default_topic(subject, "Religious Texts")
        self.confirm_default_topic(subject, "Religious Rituals and Practices")
        self.confirm_default_topic(subject, "Religious Ethics and Morality")
        self.confirm_default_topic(subject, "Religious Philosophy")
        self.confirm_default_topic(subject, "Comparative Religion")
        self.confirm_default_topic(subject, "Sociology of Religion")
        self.confirm_default_topic(subject, "Psychology of Religion")
        self.confirm_default_topic(subject, "History of Religion")
        self.confirm_default_topic(subject, "Gender and Religion")

        subject = self.confirm_default_subject('Social Studies Education')

        self.confirm_default_topic(subject, "Culture")
        self.confirm_default_topic(subject, "Economics")
        self.confirm_default_topic(subject, "History")
        self.confirm_default_topic(subject, "Law social studies topics")
        self.confirm_default_topic(subject, "Critical thinking")
        self.confirm_default_topic(subject, "Science and technology studies")
        self.confirm_default_topic(subject, "Authority and governments")
        self.confirm_default_topic(subject, "Civic ideas")
        self.confirm_default_topic(subject, "Civics")
        self.confirm_default_topic(subject, "Environmental education")
        self.confirm_default_topic(subject, "Identity")
        self.confirm_default_topic(subject, "Institutions and groups")
        self.confirm_default_topic(subject, "Globalization")

        subject = self.confirm_default_subject('Social Work')

        self.confirm_default_topic(subject, "Counseling skills")
        self.confirm_default_topic(subject, "Trauma-informed care")
        self.confirm_default_topic(subject, "Mental health disorders")
        self.confirm_default_topic(subject, "Substance abuse treatment")
        self.confirm_default_topic(subject, "Grief and loss counseling")
        self.confirm_default_topic(subject, "Crisis intervention")
        self.confirm_default_topic(subject, "Family dynamics and systems theory")
        self.confirm_default_topic(subject, "Child abuse and neglect")
        self.confirm_default_topic(subject, "Domestic violence intervention")
        self.confirm_default_topic(subject, "Parenting education")
        self.confirm_default_topic(subject, "Divorce and separation support")
        self.confirm_default_topic(subject, "Social policy analysis")
        self.confirm_default_topic(subject, "Advocacy and social change")
        self.confirm_default_topic(subject, "Community organizing and development")
        self.confirm_default_topic(subject, "Social justice issues")
        self.confirm_default_topic(subject, "Macro practice interventions")
        self.confirm_default_topic(subject, "Older adults and gerontology")
        self.confirm_default_topic(subject, "People with disabilities")
        self.confirm_default_topic(subject, "LGBTQ+ community")
        self.confirm_default_topic(subject, "Homeless individuals")
        self.confirm_default_topic(subject, "Immigrant and refugee populations")
        self.confirm_default_topic(subject, "Ethical decision making")
        self.confirm_default_topic(subject, "Professional boundaries")
        self.confirm_default_topic(subject, "Case management")
        self.confirm_default_topic(subject, "Documentation and reporting")
        self.confirm_default_topic(subject, "Supervision and consultation")

        subject = self.confirm_default_subject('Sociology')

        self.confirm_default_topic(subject, "The Impact of Social Media on Social Interactions")
        self.confirm_default_topic(subject, "Gender Inequality in the Workplace")
        self.confirm_default_topic(subject, "Race and Policing")
        self.confirm_default_topic(subject, "Migration and Identity Formation")
        self.confirm_default_topic(subject, "Health Disparities in Underserved Communities")
        self.confirm_default_topic(subject, "Family Structures and Dynamics")
        self.confirm_default_topic(subject, "Environmental Justice")
        self.confirm_default_topic(subject, "Education and Social Mobility")
        self.confirm_default_topic(subject, "Urbanization and Social Change")
        self.confirm_default_topic(subject, "Technology and Society")

        subject = self.confirm_default_subject('Therapeutic Recreation')

        self.confirm_default_topic(subject, "The therapeutic recreation process (assessment, planning, implementation, evaluation)")
        self.confirm_default_topic(subject, "Leisure education and skill development")
        self.confirm_default_topic(subject, "Client-centered care and strengths-based approach")
        self.confirm_default_topic(subject, "Ethical considerations in therapeutic recreation")
        self.confirm_default_topic(subject, "Leisure diagnostic tools")
        self.confirm_default_topic(subject, "Functional assessments for physical, cognitive, social, and emotional needs")
        self.confirm_default_topic(subject, "Outcome measurement and goal setting")
        self.confirm_default_topic(subject, "Adapted recreation activities for specific populations")
        self.confirm_default_topic(subject, "Outdoor recreation therapy")
        self.confirm_default_topic(subject, "Creative arts therapies (music, art, drama)")
        self.confirm_default_topic(subject, "Aquatic therapy")
        self.confirm_default_topic(subject, "Cognitive stimulation activities")
        self.confirm_default_topic(subject, "Social skills development through recreation")
        self.confirm_default_topic(subject, "Individuals with physical disabilities")
        self.confirm_default_topic(subject, "Individuals with mental health conditions")
        self.confirm_default_topic(subject, "Older adults")
        self.confirm_default_topic(subject, "Children and youth")
        self.confirm_default_topic(subject, "Individuals with developmental disabilities")
        self.confirm_default_topic(subject, "Psychology and human behavior")
        self.confirm_default_topic(subject, "Anatomy and physiology")
        self.confirm_default_topic(subject, "Sociology and community dynamics")
        self.confirm_default_topic(subject, "Medical terminology")
        self.confirm_default_topic(subject, "Documentation and reporting")
        self.confirm_default_topic(subject, "Collaboration with other healthcare professionals")
        self.confirm_default_topic(subject, "Advocacy for leisure access and rights")
        self.confirm_default_topic(subject, "Ethical practice and professional standards")

        subject = self.confirm_default_subject('Urban and Regional Studies')

        self.confirm_default_topic(subject, "Urban planning")
        self.confirm_default_topic(subject, "Planning")
        self.confirm_default_topic(subject, "Real estate and development")
        self.confirm_default_topic(subject, "Transport")
        self.confirm_default_topic(subject, "Local government")
        self.confirm_default_topic(subject, "Environmental design")
        self.confirm_default_topic(subject, "Government administration")
        self.confirm_default_topic(subject, "Processes of urbanization and city life")
        self.confirm_default_topic(subject, "Sustainability")
        self.confirm_default_topic(subject, "Urban economics")
        self.confirm_default_topic(subject, "Urban infrastructures and mobility")

        subject = self.confirm_default_subject('Veterinary Medicine')

        self.confirm_default_topic(subject, "Animal welfare")
        self.confirm_default_topic(subject, "Animal nutrition")
        self.confirm_default_topic(subject, "Regulatory medicine")
        self.confirm_default_topic(subject, "Anatomy and physiology")
        self.confirm_default_topic(subject, "Diagnostic and problem-solving")
        self.confirm_default_topic(subject, "Surgical proficiency")
        self.confirm_default_topic(subject, "Compassionate patient care")
        self.confirm_default_topic(subject, "Interpersonal and professional communication")

        subject = self.confirm_default_subject('Women and Gender Studies')

        self.confirm_default_topic(subject, "Indigenous feminism")
        self.confirm_default_topic(subject, "Gender and science")
        self.confirm_default_topic(subject, "Gender and Sexuality Studies")
        self.confirm_default_topic(subject, "Gendered violence")
        self.confirm_default_topic(subject, "Masculinities")
        self.confirm_default_topic(subject, "Bodies and sexualities")
        self.confirm_default_topic(subject, "Feminism and knowledge")
        self.confirm_default_topic(subject, "Feminist geographies")
        self.confirm_default_topic(subject, "Queer theory")
        self.confirm_default_topic(subject, "Sexuality")
        self.confirm_default_topic(subject, "Social justice")
        self.confirm_default_topic(subject, "Sociology of gender")
        self.confirm_default_topic(subject, "Women's History")

    def confirm_user_orgs(self):
        import random

        print(f"confirm_user_orgs()...")
        from api.models.user_org import UserOrg
        from api.models.org import Org
        from django.contrib.auth.models import User
        from api.models.facility import Facility
        try:
            admin = User.objects.filter(username='jitguruadmin').first()

            orgCommunity = Org.objects.filter(name='jitguru org:community').first()
            if orgCommunity is None:
                orgCommunity = Org.objects.create(name='jitguru org:community')

            orgCommunityDict = model_to_dict(orgCommunity, fields=[field.name for field in orgCommunity._meta.fields])
            userOrgs = UserOrg.objects.filter(org_id=orgCommunityDict["id"], user_id=admin.id).first()
            if userOrgs is None:
                UserOrg.objects.create(user_id=admin.id, org_id=orgCommunityDict["id"])

            orgFacility = Org.objects.filter(name='jitguru org:1 facility').first()
            if orgFacility is None:
                orgFacility = Org.objects.create(name='jitguru org:1 facility')
            if orgFacility is not None:
                orgFacilityDict = model_to_dict(orgFacility, fields=[field.name for field in orgFacility._meta.fields])
                userOrgs = UserOrg.objects.filter(org_id=orgFacilityDict["id"], user_id=admin.id).first()
                if userOrgs is None:
                    userOrg = UserOrg.objects.create(user_id=admin.id, org_id=orgFacilityDict["id"])
                # create the one facility for this org. ergo... orgFacilityFacility
                orgFacilityDict = model_to_dict(orgFacility, fields=[field.name for field in orgFacility._meta.fields])
                facility = Facility.objects.filter(org_id=orgFacilityDict['id']).first()
                if facility is None:
                    facility = Facility.objects.create(org_id=orgFacilityDict['id'],name='jitguru facility: millhouse', description='singleton facility of jitguru org: facility')

            orgMultifacility = Org.objects.filter(name='jitguru org:multifacility').first()
            if orgMultifacility is None:
                orgMultifacility = Org.objects.create(name='jitguru org:multifacility')
            if orgMultifacility is not None:
                orgMultifacilityDict = model_to_dict(orgMultifacility, fields=[field.name for field in orgMultifacility._meta.fields])
                userOrgs = UserOrg.objects.filter(org_id=orgMultifacilityDict["id"], user_id=admin.id).first()
                if userOrgs is None:
                    UserOrg.objects.create(user_id=admin.id, org_id=orgMultifacilityDict["id"])
                # create the facilitys for this org.
                orgMultifacilityDict = model_to_dict(orgMultifacility, fields=[field.name for field in orgMultifacility._meta.fields])
                facilitys = Facility.objects.filter(org_id=orgMultifacilityDict['id'])
                if facilitys is None or len(facilitys) == 0:
                    facility = Facility.objects.create(org_id=orgMultifacilityDict['id'],name='jitguru facility: henhouse', description='1/3 of multifacility')
                    facility = Facility.objects.create(org_id=orgMultifacilityDict['id'],name='jitguru facility: woodshed', description='2/3 of multifacility')
                    facility = Facility.objects.create(org_id=orgMultifacilityDict['id'],name='jitguru facility: hayshed', description='3/3 of multifacility')

            gurua = User.objects.get(username="gurua")
            gurub = User.objects.get(username="gurub")
            guruc = User.objects.get(username="guruc")

            pupila = User.objects.get(username="pupila")
            pupilb = User.objects.get(username="pupilb")
            pupilc = User.objects.get(username="pupilc")

            jitguruadmin = User.objects.get(username='jitguruadmin')
            jitguruadmin_orgs = UserOrg.objects.filter(user_id=jitguruadmin.id)

            gurua_orgs = UserOrg.objects.filter(user_id=gurua.id)
            gurub_orgs = UserOrg.objects.filter(user_id=gurub.id)
            guruc_orgs = UserOrg.objects.filter(user_id=guruc.id)

            pupila_orgs = UserOrg.objects.filter(user_id=pupila.id)
            pupilb_orgs = UserOrg.objects.filter(user_id=pupilb.id)
            pupilc_orgs = UserOrg.objects.filter(user_id=pupilc.id)

            orgs_to_assign = random.choices(Org.objects.all(), k=5)

            if len(jitguruadmin_orgs) < 5:
                for org in orgs_to_assign:
                    self.confirm_user_org(jitguruadmin, org)

            if len(gurua_orgs) < 5:
                for org in orgs_to_assign:
                    self.confirm_user_org(gurua, org)

            if len(gurub_orgs) < 5:
                for org in orgs_to_assign:
                    self.confirm_user_org(gurub, org)

            if len(guruc_orgs) < 5:
                for org in orgs_to_assign:
                    self.confirm_user_org(guruc, org)

            if len(pupila_orgs) < 5:
                for org in orgs_to_assign:
                    self.confirm_user_org(pupila, org)

            if len(pupilb_orgs) < 5:
                for org in orgs_to_assign:
                    self.confirm_user_org(pupilb, org)

            if len(pupilc_orgs) < 5:
                for org in orgs_to_assign:
                    self.confirm_user_org(pupilc, org)




        except Exception as e:
            print(f"unable to confirm user orgs: {e}")

    def confirm_user_org(self, user, org):
        from api.models.user_org import UserOrg

        already = UserOrg.objects.filter(user=user, org=org)
        if len(already) == 0:
            created = UserOrg.objects.create(user=user, org=org)

    def confirmDefaultGroupPermissions(self):
        print(f"confirmDefaultGroupPermissions()...")
        from django.contrib.auth.models import Group
        from django.contrib.auth.models import Permission
        from django.contrib.auth.models import User
        try:
            admins = Group.objects.filter(name="admins").first()
            admin = User.objects.filter(username="jitguruadmin").first()

            assign_org_to_self = Permission.objects.filter(codename="assign_org_to_self").first()
            add_org = Permission.objects.filter(codename="add_org").first()
            add_facility = Permission.objects.filter(codename="add_facility").first()

            admins.permissions.add(assign_org_to_self)
            admins.permissions.add(add_org)
            admins.permissions.add(add_facility)

            admin.groups.add(admins)
        except Exception as e:
            print(f"unable to conrirm default group permissions: {e}")

    def confirmDefaultPermissions(self):
        print(f"confirmDefaultPermissions()...")
        from django.contrib.auth.models import Permission
        try:
            found = Permission.objects.filter(codename="assign_org_to_self").first()
            if found is None:
                created = Permission.objects.create(codename="assign_org_to_self", content_type_id=17, name="Can assign org to self")
                if created is not None:
                    print(f"created permission: assign_org_to_self")
        except Exception as e:
            print(f"unable to confirm default permissions: {e}")

    def confirn_default_groups(self):
        print(f"confirm_default_groups...")
        from django.contrib.auth.models import Group

        admins = Group.objects.filter(name="admins")
        if len(admins) == 0:
            created = Group.objects.create(name="admins")

    def create_common_user(self, username, email, password):
        environment = os.getenv('ENVIRONMENT')
        if environment == 'local':
            from django.contrib.auth.models import User
            created = User.objects.create_user(username, email, password)
            created.last_name = 'common'
            created.first_name = 'user'
            created.save()
            return created
        else:
            print(f"no common user available for environment: {environment}")
            return None

    def confirm_default_user(self, username: str, password: str, last_name: str, first_name: str):
        from api.models.person import Person
        from api.models.user_person import UserPerson
        from django.contrib.auth.models import User

        try:
            print(f"{f"confirming user":32}: {username}")
            created = None
            found = None
            confirmable = None
            try:
                found = User.objects.get(username=username)
                if not found:
                    print(f"{f"confirming user {username}":32}: not found, creating...")
                    created = self.create_common_user(username, 'admin@jitguru.com', password)
                else:
                    print(f"{f"":32}: ok: {found.id}")
            except Exception as not_found_e:
                print(f"{f"confirming user":32}: not found, creating...")
                created = self.create_common_user(username, 'admin@jitguru.com', password)

            if created:
                print(f"{f"":32}: ok: {created.id}")
                confirmable = created
            elif found:
                print(f"{f"":32}: ok: {found.id}")
                confirmable = found
            else:
                print(f"{f"":32}: fail: for previous errors")
                return

        #     confirm user person
            user_person = None
            try:
                user_person = UserPerson.objects.get(user_id=confirmable.id)
            except Exception as user_person_e:
                pass
            if not user_person:
                person = Person.objects.create(user=confirmable, last_name=last_name,  first_name=first_name)
                UserPerson.objects.create(user=confirmable, person=person)
            return confirmable

        except Exception as user_e:
            print(f"error confirming user: {username}: {user_e}")

    def confirm_admin_user(self):
        from django.contrib.auth.models import User

        try:
            found = User.objects.filter(username="jitguruadmin").first()
            if found is None:
                created = User.objects.create_user("jitguruadmin", "admin@jitguru.com", "ilovethejitguru")
                if created is not None:
                    print(f"created default user: {created.username}")
                    created.is_superuser = True
                    created.is_staff = True
                    created.last_name = 'jitguru'
                    created.first_name = 'admin'
                    created.save()
        except Exception as e:
            print(f"unable to confirm default user: {e}")

        try:
            found = User.objects.filter(username="jitguruadmin").first()
            if found is None:
                created = User.objects.create_user("jitguruadmin", "admin@jitguru.com", "ilovethejitguru")
                if created is not None:
                    print(f"created default user: {created.username}")
                    created.is_superuser = True
                    created.is_staff = True
                    created.last_name = 'jitguru'
                    created.first_name = 'admin'
                    created.save()
        except Exception as e:
            print(f"unable to confirm default user: {e}")


    def confirm_default_users(self):
        print(f"confirm_default_users...")
        from django.contrib.auth.models import User
        password = os.getenv('DEFAULT_PASSWORD')
        username = os.getenv('DEFAULT_USERNAME')

        self.confirm_admin_user()
        mcdude = self.confirm_default_user(username, password, "mcdude", "das_dudin")
        guru_a = self.confirm_default_user("gurua", password, "guru_a", "alpha")
        guru_b = self.confirm_default_user("gurub", password, "guru_b", "bravo")
        guru_c = self.confirm_default_user("guruc", password, "guru_c", "charlie")

        pupil_a = self.confirm_default_user("pupila", password, "pupil_a", "angus")
        pupil_b = self.confirm_default_user("pupilb", password, "pupil_b", "beaner")
        pupil_c = self.confirm_default_user("pupilc", password, "pupil_c", "chowder")


    def confirm_default_org(self, name, description):
        print(f"confirm_default_org({name})...")
        from api.models.org import Org
        try:
            found = Org.objects.filter(name=name).first()
            if found == None:
                created = Org.objects.create(name=name)
                if created is not None:
                    print(f"created org: {created.name}")
                    created.description = description
                    created.save()
                else:
                    print(f"unable to create default org: {name}")
        except Exception as e:
            print(f"unable to confirm default org {name}: {e}")

    def confirm_default_orgs(self):
        import csv
        from api.models.org import Org

        print(f"confirm_default_orgs...")
        self.confirm_default_org('jitguru:community', "demonstrates distributed instruction and learning without a facility")
        self.confirm_default_org('jitguru:facility', "demonstrates distributed instruction and learning centered in one physical faciliity")
        self.confirm_default_org('jitguru:multifacility', "demonstrates distributed instruction and learning centered more than one physical faciliity")

        if Org.objects.all().count() < 4:

            folder = os.path.join(os.getcwd(), "resource", "ODEF_v2.1_EN")
            filepath = os.path.join(folder, "ODEF_v2_1.csv")
            with open(filepath) as source:
                reader = csv.reader(source)
                for row in reader:
                    index = row[0]
                    source_id = row[1]
                    name = row[2]
                    facility_type = row[3]
                    authority_name = row[4]
                    isced010 = row[5]
                    isced020 = row[6]
                    isced1 = row[7]
                    isced2 = row[8]
                    isced3 = row[9]
                    isced4plus = row[10]
                    olms_status = row[11]
                    full_addr = row[12]
                    unit = row[13]
                    street_no = row[14]
                    street_name = row[15]
                    city = row[16]
                    prov_terr = row[17]
                    postal_code = row[18]
                    pruid = row[19]
                    csdname = row[20]
                    csduid = row[21]
                    longitude = row[22]
                    latitude = row[23]
                    geo_source = row[24]
                    provider = row[25]
                    cmaname = row[26]
                    cmauid = row[27]
                    alreadys = Org.objects.filter(name__iexact=name)
                    if len(alreadys) == 0:
                        created = Org.objects.create(
                            name=name,
                            facility_type=facility_type,
                            authority_name=authority_name,
                            isced010=isced010,
                            isced020=isced020,
                            isced1=isced1,
                            isced2=isced2,
                            isced3=isced3,
                            isced4plus=isced4plus,
                            olms_status=olms_status,
                            full_addr=full_addr,
                            unit=unit,
                            street_no=street_no,
                            street_name=street_name,
                            city=city,
                            prov_terr=prov_terr,
                            postal_code=postal_code,
                            pruid=pruid,
                            csdname=csdname,
                            csduid=csduid,
                            longitude=longitude,
                            latitude=latitude,
                            geo_source=geo_source,
                            provider=provider,
                            cmaname=cmaname,
                            cmauid=cmauid,
                        )
























"""
'38a0123e19d42c1636d9'
'761013'
'Sainte-Germaine-Cousin'
'Public'
'..'
'..'
'1'
'1'
'0'
'0'
'0'
'0'
'1880
48e Avenue MontrÈal H1A2Y6'
''
'1880'
'48e avenue'
'MontrÈal'
'QC'
'H1A2Y6'
'24'
'MontrÈal'
'2466023'
'-73.501651'
'45.667625'
'Source'
'Province of QuÈbec'
'MontrÈal'
'462'
                
                """