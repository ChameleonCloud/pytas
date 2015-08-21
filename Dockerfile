FROM ipython/notebook

MAINTAINER Matthew R Hanlon <mrhanlon@tacc.utexas.edu>

COPY . /pytas
RUN cd /pytas && pip install -r requirements.txt
COPY notebooks /notebooks
