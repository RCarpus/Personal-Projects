project_number = '123456'
engineer_1_name = 'Ryan Carpus' #Your full name plus suffix
engineer_1_title = 'Staff Engineer'
engineer_1_signature = 'ryan_carpus.jpg' #Type None if you will add signature later
engineer_2_name = 'John Doe' #Project Manager full name plus suffix
engineer_2_title = 'Project Manager'
engineer_2_signature = 'ryan_carpus.jpg' #Type None if you will add signature later
initials = 'RPC/RPC/rpc' #initials of first and second engineer uppercase, plus admin in lowercase

client_prefix = 'Mr.'
client_first_name = 'John'
client_last_name = 'Deer'
client_suffix = None #Example if not None: 'P.E.'
client_company = 'ABC Client Company'
client_street_address = '123 Client Lane'
client_city = 'Clientville'
client_state = 'Michigan'
client_zip = '48xxx'

project_name = 'Proposed Commercial Building Project'
project_street_address = '5534 Project Street'
project_city = 'Pretendville'
project_state = 'Michigan'
project_zip = '48xxx'

#finish the sentence: We understand the project will consist of
#If your description includes a single quote character, preface it with a backslash
#or wrap the whole description in double quotes instead.
project_description = 'the construction of a pretend building that does not exist and will never exist.'

#True or False, first letter capitalized
has_earthwork = True
has_foundation = True
has_site_concrete = True
has_masonry = True
has_steel = True
has_bituminous = True

full_day = '700' #Input all rates as whole numbers with single quotes
half_day = '500'
overtime_hour = '100'

document_name = '123456.qc.proposal.docx' #File name for propsal, including .docx extension

'''
DO NOT MODIFY ANYTHING AFTER THIS LINE
'''

class work_type:
    '''
    Holds similar properties for each work type. 
    '''
    def __init__(self, name, file):
        self.name = name

        with open(file, 'r') as f:
            lines = f.read().splitlines()
            self.heading = lines[0]
            lines.pop(0)
            self.body = lines


with open('personnel.txt', 'r') as f:
    lines = f.read().splitlines()
    personnel_header = lines[0]
    personnel_body = lines[1]

with open('scope.txt', 'r') as f:
    lines = f.read().splitlines()
    scope_header = lines[0]
    scope_body = lines[1]

work_types = []
if has_earthwork == True:
    work_types.append(work_type('earthwork operations and underground utilities', 'earthwork.txt'))
if has_foundation == True:
    work_types.append(work_type('foundation construction', 'foundation.txt'))
if has_site_concrete == True:
    work_types.append(work_type('site concrete', 'site_concrete.txt'))
if has_masonry == True:
    work_types.append(work_type('masonry', 'masonry.txt'))
if has_steel == True:
    work_types.append(work_type('structural steel', 'steel.txt'))
if has_bituminous == True:
    work_types.append(work_type('bituminous paving operations', 'bituminous.txt'))

with open('budget_explanation.txt', 'r') as f:
    budget_explanation = f.read()

with open('terms_and_conditions.txt', 'r') as f:
        lines = f.read().splitlines()
        terms_and_conditions_header = lines[0]
        lines.pop(0)
        terms_and_conditions_body = lines

