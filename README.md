# CV Generator
Modifying your CV every time you obtain a new diploma or publish a new article can be tedious and time-wasting, even 
when using a document generator such as LaTeX.

In this project, I propose a solution to generate your CV automatically using a non-formatted `.json` or `.yaml` file
. You won't have to deal with graphical/text editors or with LaTeX code anymore, just editing that main global file 
will be enough to obtain your updated CV.

## How does it work
The idea behind this lightweight project is to separate the content and the template of our _curriculum vitae_ (such 
as in web/app development). To do so:

* First, you must write your resume using the required format. You can choose between doing it in a `.json` file or a
 `.yaml` file, however both documents must follow the schema provided in the document `cv.schema.json`.
* With your resume in plain text created, execute the code as exposed next. This will internally transform the 
previous file to a theme-specific `.tex` file.
* That `.tex` file is compiled into a PDF document using `pylatex` and saved inside `./generated_documents`.

## How to write my resume
In order to read the data and understand the content of it, you must create your document with the same format of the
 examples (`cv.example.json` and `cv.example.yaml`).

To validate the input, the project uses [JSON Schema](https://json-schema.org/) against the file `cv.schema .json`. 
It is recommended to read about it and understand all the fields. Notice that, if the provided document is not valid,
 the execution will finish with an error and the document will not be generated. No details of the exact error are 
 provided in the current version of the project, so you will have to debug it line-by-line.

## How to execute the code
First of all, install the dependencies required by the project. You can do it using `pip` as:

```
pip install -r requirements.txt
```

Then, to execute the code, we must **call the module** directly using the `-m` argument of Python. The following 
snippet summarizes the available arguments:

```
Usage:
    python -m cv_generator --cv-file <cv_file_path> --theme <theme_name> [--filename <cv_filename>] [--keep-tex]

Options:
    --cv-file <cv_file_path>    Relative or absolute path to the resume .json or .yaml file
    --theme <theme_name>        Name of the theme to use to generate the resume
    --filename <cv_filename>    Name of the generated file, without extension
    --keep-tex                  Do not remove the .tex file used to generate the resume
```

**Note**: in order to call a module, we must either execute the command in its parent directory or at least have it 
on the `PYTHONPATH`.

For example, if we execute the command:

```
python -m cv_generator --cv-file cv.example.json --theme sitges --filename example-cv
```

It uses the `cv.example.json` file as data input and formats it using the `sitges` theme. The output file will be 
stored in `./generated_documents/example-cv.pdf`.

## Available themes and examples
Only two themes are available at the moment:

|Theme Name (`<theme_name>`)|Example|Source|
|-|-|-|
|Sitges (`sitges`)|[Example](https://storage.googleapis.com/davidalvarezdlt/cv-generator-theme-sitges.pdf)|Self-designed|
|Developer CV (`developer`)|[Example](https://storage.googleapis.com/davidalvarezdlt/cv-generator-theme-developer.pdf)|[LaTeXTemplates.com](https://www.latextemplates.com/template/developer-cv)|

## Contribute
I encourage open sources lovers to implement your own design and to send a pull request so we can all benefit from it. 
However, please make sure that the code follows the same structure and that it handles possible missing fields.

