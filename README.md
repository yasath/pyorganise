## pyorganise
A Python tool to organise messy folders.

<img src="https://raw.githubusercontent.com/yasath/pyorganise/master/images/mac_ui.png" alt="Screenshot of program's UI on macOS" width="480"/>

### Current features
- [x] Moves files into neat folders and subfolders **based only on filetype**
- [x] Detailed database of filetypes and their categories (`format_classification.py`)
- [x] Entirely cross-platform with native GUI elements, including folder-picker
- [x] Copy mode as well as move mode, so files can just be copied
- [x] Subfolder mode to maintain existing organised subfolders
- [x] Dynamic renaming and categorisation of documents based on date created
- [x] Categorisation of JPEG and TIFF images based on the device and date they were taken on
- [x] ID3 tagging of music files using AcoustID

### Planned features
- [ ] Allowing users to add custom filetypes and categories to the database
- [ ] 'Undo' button to move files back into their original places
- [ ] Allowing `pyorganise` to be imported as a function in other Python programs
- [ ] *(Not in foreseeable future)* Using AcoustID fingerprints to identify and delete duplicate audio files, and keeping the higher quality option
- [ ] *(Not in foreseeable future)* Identifying and deleting duplicate image files, and keeping the higher quality option
- [ ] *(Not in foreseeable future)* Allowing the filetype database to be updated online regularly
