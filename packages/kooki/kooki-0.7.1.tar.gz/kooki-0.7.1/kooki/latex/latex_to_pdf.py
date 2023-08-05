import subprocess, os, shutil, tempfile

from kooki.tools import write_file
import pretty_output


def latex_to_pdf(name, content):

    pretty_output.start_step('pdf')
    infos = []

    temp_dir = tempfile.mkdtemp()

    tex_file_name = '{0}.tex'.format(name)
    pdf_file_name = '{0}.pdf'.format(name.split('/')[-1])
    relative_output_path = '/'.join(name.split('/')[:-1])
    absolute_output_path = os.path.join(os.getcwd(), relative_output_path)

    tex_file_path = os.path.join(temp_dir, tex_file_name)
    pdf_file_path = os.path.join(temp_dir, pdf_file_name)

    write_file(tex_file_path, content)

    command = 'xelatex -interaction=nonstopmode -halt-on-error -output-directory={1} {0}'.format(tex_file_name, temp_dir)
    log_file = os.path.join(temp_dir, 'xelatex.log')

    with open(log_file, "w") as f:
        subprocess.call(command, shell=True, stdout=f)
        subprocess.call(command, shell=True, stdout=f)

    if pretty_output._debug_policy:
        pretty_output.info('XeLaTeX output: cat {0}'.format(log_file))

    if os.path.isfile(pdf_file_path):
        shutil.copy(pdf_file_path, absolute_output_path)
        infos.append({'name': pdf_file_name, 'status': '[created]', 'info': ''})
    else:
        infos.append({'name': pdf_file_name, 'status': ('[missing]', 'red'), 'info': ''})

    pretty_output.infos(infos, [('name', 'blue'), ('status', 'green'), ('info', 'cyan')])
