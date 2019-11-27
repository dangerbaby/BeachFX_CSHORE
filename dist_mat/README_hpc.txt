
The hpc addition is designed to permit parallel CSHORE runs on the
HPC.  The workflow includes local creation of infiles, execution of
CSHORE on the HPC, and then local postprossesing.

1)Edit the PBS script entitiled submit_script_onyx.pbs.  An estimate
of the maximum expected time required to run you batch of CSHORE runs
is required as the walltime variable.  To permit a run of up to 2
hours, for instance, use the following:

#PBS -l walltime=2:00:00

The computational expense is charged to a project ID thta is indicated
in the script. You can use the show_usage command to find the projects
that are available to you and their associated project IDs. In the
show_usage output, project IDs appear in the column labeled
"Subproject."  Modify the scipt to reflect the Project ID for your
job, including the following directive:

#PBS -A Project_ID

2)Execute make_cshore_infiles in the manner outlined within
README.txt.  This will create a new gzipped tar file named to_hpc.tgz.


3)Copy to_hpc.tgz to the HPC, either with the scp or the file uplaod
capability of the HPC portal.  unzip and untar at hte command line on
onyx:

user@onyx09:~> tar -zxvf to_hpc.tgz

submit the job:

user@onyx09:~> qsub submit_script_onyx.pbs

At completion, the file run_all_output.txt will show the results of
the run and from_hpc.tgz is created.  Copy from_hpc.tgz back to the
local machine being certian that the from_hpc.tgz is in the same
directory as the to_hpc.tgz file

4) Execute make_dat file: All CSHORE results are discovered and a
separate dat file designed for use with BeachFX is created for each
reach.






