FROM ipython/notebook

MAINTAINER Matthew R Hanlon <mrhanlon@tacc.utexas.edu>

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /pytas
COPY notebooks /notebooks
