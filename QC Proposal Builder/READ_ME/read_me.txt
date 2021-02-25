QC Proposal Builder
Author: Ryan carpus
Last Revision: 2021-02-24

**********This program writes a propsosal for construction quality control testing. The text files used to create the word document have been edited from how I use them at work for confidentiality. This project has no use outside of the specific context I use it at work, but it demonstrates knowledge of using Python to automate document creation, so that's cool I guess.***********

To use this program, edit the parameters in the config.py file using a text editor or IDE.
Use the estimate_sheet.xlsx file to build your estimate. If you need to add a new unit with unit cost,
add a new line to worksheet 2, then modify the conditional formatting for the dropdown menu on worksheet 1 to include the new line.
Do not populate any cells on worksheet 1 outsite of the estimate table.
Modify the lab_unit_rates.xlsx file to include lab tests that should be within the scope of the project.
Again, do not populate any cells outside the table.
Copy the image files for your signature and for the project manager's signature into the same directory with the rest of these files.
When you are ready to build your proposal, run the build_qc_propsal.py file. Your proposal will appear in the folder with the rest of the files.

Do not rename any files (except the file name of the proposal after you build it).

Do not modify the build_qc_propodal.py file. This could break program.

Do not modify anything in the config.py file after the line that says "Do not modify anything after this line".

You may modify the descriptions for work types by opening the .txt files and adding, removing, or changing paragraphs.
Each bullet point for a work item is a new paragraph. Keep the formatting the same as it is, or it will not look right when you build the proposal.

Modifying .txt files other than the specific work items could could unintended results. If you need to modify the text of anything else in the proposal,
it would be best to modify the file in Word after building it, or ask Ryan Carpus for help on how to modify the python files.