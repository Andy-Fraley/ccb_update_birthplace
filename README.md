# ccb_update_birthplace
Quickie project to pull birthplace info out of process notes field and push into custom "Birthplace" field

This quickly-developed utility set was used to pull Birthplace data out of "Baptism Coordination" process
queue notes (for "Record Completion Information" step) and update them into a new Individual custom field named
"Birthplace" (aka "udf_text_5").

To do the extraction from notes fields and then load into custom field "Birthplace", do the following steps:
- Run ./get_place_of_birth.py --dump NOTES (this will pull all notes including private notes)
- Take output file notes_<date_timestamp>.xml and move into "data_files" subdirectory
- Run awk -f pob.awk data_files/notes_<date_timestamp>.xml >data_files/notes_<date_timestamp>_pob.tsv
- Run ./load_pobs_into_ccb.py --input-id-pob-tsv-filename data_files/notes_<date_timestamp>_pob.tsv

NOTE - The ./load_pobs_into_ccb.py utility uses Python requests library to do the POST update_individual
