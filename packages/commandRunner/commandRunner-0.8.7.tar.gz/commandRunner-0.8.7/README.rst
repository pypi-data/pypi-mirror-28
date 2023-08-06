commandRunner
=============

commandRunner is yet another package created to handle running commands,
scripts or programs on the command line targetted at thread safe execution
for Celery. The simplest class lets you run anything locally on your machine.
Other classes are targeted at Analytics and data processing platforms such as
Grid Engine (and eventually HADOOP). The class attempts to run commands in a
moderately threadsafe way by requiring that you provide it with sufficient
information that it can build a uniquely labeled temporary directory for all
input and output files. This means that this can play nicely with things like
Celery workers.

Installation
------------

You can install the required python modules with pip using the included
requirements.txt file.

If using R you must have a recent >3.0.0 installation of R and its development
libraries.

If you are using the DRMAA support you must be able to set the environment
variables

DRMAA_LIBRARY_PATH
SGE_ROOT

Release 0.8.7
-------------

This release supports running commands on local unix shell and DRMAA compliant grid
engine installs (ogs, soge and univa) and it can also run strings of python
code.  Commands are built/interpolated via some simple rules described below.

Future
------

In the future we'll provide classes to run commands over Hadoop, Octave, and
SAS Server.

Binary Execution Usage
----------------------

geRunner and localRunner are capable of executing arbitrary binaries as
though run in a unix shell

This is the basic usage for running a binary using the local unix shell::

    from commandRunner.localRunner import *

    r = localRunner(tmp_id="ID_STRING", tmp_path=,/tmp/", out_glob=['file', ],
                    command="ls /tmp", input_data={DATA_DICT})
    r.prepare()
    exit_status = r.run_cmd(success_params=[0])
    r.tidy()
    print(r.output_data)

__init__ initalises all the class variables needed and performs the command
string interpolation which allow you to parameterise the command.

Interpolation rules work the following way. The command string is split in to
tokens. The tokens are serched for specific control flags the define inputs,
output, paths and command parameters. Take the following call::

    r = localRunner(tmp_id="ID_STRING",
                    tmp_path="/tmp/",
                    in_glob=['.in', ]
                    out_glob=['.file', ],
                    params=["-a","-l", "b"]
                    param_values={'b': {'value': 'this',
                                   'spacing': True,
                                   'switchless': False},
                             }
                    command="ls $P1 $P2 $P$ /tmp",
                    input_data={'input.in': 'some input data'},
                    std_out_str="file.stdout",
                    identifier="string"
                    env_vars={"str":"str"},
                    debug=False,)

This effectively builds the following command::

      ls -a -l b this /tmp > file.stdout

Command string interpolation accepts a range of control sequences which begin
with $.

If you provide a list of strings via the in_glob function variable these
will be made availabe in the command string using $I[int]. tmp_id string and
each sequential entry in the in_glob list are concatenated. For tmp_id="this"
and in_glob=[".in", ".thing", ] two strings are created this.in and this.thing
and they can be refered to in the command string as $I1 and $I2.

A near identical interpolation is carried out for the out_glob list providing
$O[int]. With tmp_id="this" and out_glob=['.file', ] string this.file will be
created and can be refered to in the command string as $O1.

Command line parameters are more subtle. These will be available as $P[int]
where each integer refers to a successive entry in the params list. If
param_values is not provided then the values in params will be interpolated
as the appear in the params list. If params_values is provided then more
sophisticated control of the param interpolation can be achieved. Providing
a value (12) means that a param entry ("b") will be interpolated as "b 12".
Setting spacing to false suppresses the space, "b12" and setting switchless to
True suppresses the param name "12".

We also provide a couple of convenience strings $TMP, $ID and $VALUE. There
will interpolate the contents of tmp_path, tmp_id and value_string respectively

Next it takes input_data. This is a dict of {Filename:Data_string} values.
Iterating over, it writes the data to a file given the values in temp_path and
temp_id. So given the following dict and the values above::

    { "test.file" : "THIS IS MY STRING OF DATA"}

would result in a file with the path /tmp/ID_STRING/test.file

env_vars is a dict of key:value strings which is used to set the unix
environment variables for the running command.

debug takes a boolean. this controls if the tmp directory created is world
writeable. Debug mode assumes you wish to leave behind the tmp dir to
allow other process to access or analyse it.

Note that only tmp_id, tmp_path and command are required. Omitting
input_data or out_glob assumes that there are respectively no input files to
write or output files to gather and interpolations for $I[int], $O[int] and
$P[int] will not reference anything.

The line r.run_cmd(success_params=[0]) runs the command string provided.

Once complete if out_globs have been provided and the files were output then
the contents of those files can be found in the dict r.output_data. which has
the same {Filename:Data_string} form as the input_data dict::

{ "output.file" : "THIS IS MY PROCESSED DATA"}

r.tidy() cleans up deleting any input and output files and the temporary
working directory. Any data in the output file is available in to r.output_data

Grid Engine Quirks
------------------

geRunner uses python DRMAA to submit jobs. A consequence of this that a command
string is not constructed in quite the same way. The first portion of the
command string is split off as a command. Subsequence portions are tokenised
and added to a params array to be passed to DRMAA

The Options dict is flattened to a key:value list. You can include or omit as
many of those as you'd like options as you like. Any instance of the string
$I[int] and $O[int] in final args array will be interpolated as usual

If std_out_string is provided it will be used as
a file where the Grid Engine thread STDOUT will be captured::

    from commandRunner.geRunner import *

    r = geRunner(tmp_id="ID_STRING", tmp_path="/tmp/", out_glob=['.file'],
                 command="ls -lah", input_data={"File.txt": "DATA"},
                 params = ["-file"]
                 param_values = {'-file': {'value': '$O1',
                                   'spacing': True,
                                   'switchless': False},
                                 },
                 std_out_string="std.out")
    r.prepare()
    exit_status = r.run_cmd(success_params=[0])
    r.tidy()
    print(r.output_data)

Although DRMAA functions differently you can think of this as effectively
run the following command (after following the interpolation rules)::

   ls -file out.file -lah > std.out

Script Usage
------------

commandRunner classes can also call code natively, pythonRunner will
take blocks of python code, rRunner will take blocks of R code. Both construct
a temp directory and place the input data there. Any code passed will then
execute as though is is running from the temp directory (via os.chdir).

In theory you can provide any arbitrarily large chunk of python or R code.
In practice you probably want to keeps these to short single function
scripts for less than 100 lines as debugging is quite tricky given the
layer of abstraction.

It is also worth noting that accepted code forms a dialect of both python and
R; the " character is not valid and you must use the single quote to bound
strings.

Execution by pythonRunner is somewhat different to geRunner and localRunner.
Instances of this class take a script arg and not a command arg and .prepare()
and .run_cmd() function somewhat differently::

    from commandRunner.pythonRunner import *

    r = pythonRunner(tmp_id="ID_STRING",
                    tmp_path="/tmp/",
                    in_glob=['.in', ]
                    out_glob=['.file', ],
                    params=["-a","-l", "b"]
                    param_values={'b': {'value': 'this',
                                   'spacing': True,
                                   'switchless': False},
                             }
                    script="print(str(I1.read()))",
                    input_data={'input.in': 'some input data'},
                    std_out_str="file.stdout",
                    identifier="string"
                    env_vars={"str":"str"},
                    )
    r.prepare()
    exit_status = r.run_cmd()
    r.tidy()
    print(r.output_data)

As before input_data is a dict of 'file name': 'data' pairs which will be
written to a directory specified by tmp_path+tmp_id+"/" (i.e. /tmp/ID_STRING/).
in_glob and out_glob specify a set of file handles that will be opened for you
so you do not have to open them in your provided script. in_globs should be
matched to file names in input_data. In the example above the in_glob for '.in'
will open the input.in data file and that will be available as a variable named
I1. If there were more entries in in_glob they would be named in sequence I1, I2
I3 etc... out_glob functionas as a form of promise that your script will write
to some output files. For each entry in out_glob a filehandle for writing is
opened using the tmp_id as the file name. As above O1 would open a file
called ID_STRING.file

Params are also created as variables, named P1, P2, P3, etc... These refer in
order to the values in the params list. If there is not an entry for the
param in param_values these variables are set to True. If there is an entry
in the param_values arg then the variable will be a dict with a key value
pair that gives you the name and the value. In the example above P3 is a
dict of {'b': "this"}, In this way some runtime configuration can be passed in
to the script.

Anything provided to env_vars will be add to the script environment using
additions to os.environ[]

script is an argument that takes any valid python string. In the example above
it reads the contents from the I1 filehandle ('some input data') and then
echos that to stdout. In theory you can place any sized piece of python here
but smaller scripts made up of a handful of lines are probably more
ane/sensible. Note that escape characters will need to be double escaped (\\n
not \n)

When .prepare() is called a temp directory is build and the input_data files
are written to it. Next various filehandles and param variables are composed
and appended to the provided script. Once the new script is prepared compile()
is called on it to ensure the script is a valid python string. Assuming
.prepare() is succesful you can then call .run_cmd().

run_cmd() creates a new python subprocess, runs the script in this child
process (insulating it from the namespace of the parent process) and captures
any writes to stdout and stderr.

Once complete you can find the outputs in the .output_data dict. There will
be and entry for stdout with a key named for your std_out_str. There will also
be a key for stderr named tmp_id+".err", in this example "ID_STRING.err". As
per local runner there will be a key for every file that matched the provided
out_glob list as long as the file has a non-zero size. If you do not
write to one of the provided output file handles they will not be collected
in output_data

R Scripts
---------

rRunner makes use of rpy2 to execute R code. You may need to amend your
LD_LIBRARY_PATH
https://stats.stackexchange.com/questions/6056/problems-with-librblas-so-on-ubuntu-with-rpy2

The API and broad functioning is roughly similar to the pythonRunner. Unlike
pythonRunner code is not checked for syntactic correctness before execution.
So any errors will occur at runtime for the code you provide.

File handles (I1, I2, ... and O1, O2 etc...) are available as above. These
are opened with R's base file() function. You may wish instead to override
these with things like csv.reader() where it is more convenient. Params (P1,
P2, etc...) also exist, name:value pairings are avaiable R lists() rather
than python dicts.

Anything provided to env_vars will be add to the script environment using
Sys.setenv()

Unlike the python case it is imperative you check the that the error data in
output_data is empty before assuming your R code ran successfully. As above
you can find the outputs from the stdout of your script in the output_data
variable. We leave it to you


Tests
-----

Best to run these 1 suite at a time, geRunner tests will fail if you do not
have Grid Engine installed, DRMAA_LIBRARY_PATH set and SGE_ROOT set, for example::

    export DRMAA_LIBRARY_PATH=/opt/ogs_src/GE2011.11/lib/linux-x64/libdrmaa.so
    export SGE_ROOT=/opt/ogs_src/GE2011.11/

Run tests with::

    python setup.py test -s tests/test_commandRunner.py
    python setup.py test -s tests/test_localRunner.py
    python setup.py test -s tests/test_geRunner.py
    python setup.py test -s tests/test_pythonRunner.py
    python setup.py test -s tests/test_rRunner.py

TODO
----

1. Implement hadoopRunner for running command on Hadoop
2. Implement sasRunner for a SAS backend
3. Implement octaveRunner for Octave backend
4. matlab? mathematica?
