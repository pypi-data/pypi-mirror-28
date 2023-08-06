# AutoInterOp

### Description
Automatically runs a number of Illumina InterOp processing tools on a
target MiSeq run folder. The folder should contain both an **InterOp** folder
and a **RunInfo.xml** file.

### Installation
```pip3 install AutoInterOp```

#### Dependencies
All InterOp binaries must be added to your $PATH.
- InterOp (v1.1.3): _https://github.com/Illumina/interop/releases_

AutoInterOp also depends on the Python modules found in requirements.txt.
It is suggested that you create a virtual environment and install these
modules via the following command:

```pip3 install -r requirements.txt```

### Usage
```bash
Usage: AutoInterOp.py [OPTIONS]

Options:
  -r, --run_folder PATH     Path to an Illumina MiSeq run folder. This should
                            contain a SampleInfo.xml file and an InterOp
                            folder.  [required]
  -o, --output_folder PATH  Path to desired output folder. Defaults to the
                            same place as the specified run_folder.
  -z, --zip                 Set this flag to zip all output files into a
                            single archive available within your output folder.
  --help                    Show this message and exit.
  ```