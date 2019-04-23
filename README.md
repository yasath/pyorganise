## pyorganise
A Python tool to organise messy folders.

<img src="https://github.com/yasath/pyorganise/raw/old-cli/images/CLI-Demo.gif" alt="Screen capture of program's CLI UI on macOS"/>

### Current features
- [x] Moves files into neat folders and subfolders **based only on filetype**
- [x] Only semi-complete database of filetypes and their categories (`format_classification.py`)
- [x] Copy mode as well as move mode, so files can just be copied
- [x] Entirely cross-platform

### Planned features
- [ ] User-friendly GUI with file-picker
- [ ] Allowing users to add custom filetypes and categories to the database
- [ ] Moving files into folders and subfolders **based on file metadata**
- [ ] Dynamic renaming of files based on file metadata
- [ ] ID3 tagging of music files using AcoustID
- [ ] Using AcoustID fingerprints to identify and delete duplicate audio files, and keeping the higher quality option
- [ ] Identifying and deleting duplicate image files, and keeping the higher quality option
- [ ] *(Not in foreseeable future)* Allowing the filetype database to be updated online regularly
- [ ] *(Not in foreseeable future)* Allowing `pyorganise` to be imported as a function in other Python programs
