FROM python:2.7-alpine AS builder

# Install Qooxdoo
RUN mkdir /qooxdoo
ENV QOOXDOO_PATH /qooxdoo

# Download and extract Qooxdoo
RUN wget https://github.com/qooxdoo/qooxdoo/releases/download/release_5_0_2/qooxdoo-5.0.2-sdk.zip -P /qooxdoo && \
    unzip /qooxdoo/qooxdoo-5.0.2-sdk.zip -d /qooxdoo && \
    mv /qooxdoo/qooxdoo-5.0.2-sdk/* /qooxdoo/

# Install required packages for building
RUN apk add --no-cache build-base python2-dev apache2-dev cups-dev

# Install mod_wsgi for Apache
RUN pip install --no-cache-dir mod_wsgi

# Copy source code for building
COPY . /app
WORKDIR /app

# Setup the virtual environment
RUN pip install --no-cache-dir virtualenv && \
    virtualenv venv
ENV PATH "/app/venv/bin:$PATH"

# Install dependencies
RUN pip install --no-cache-dir -r doc/requirements_py2.7.txt

# Apply settings_local.py
RUN mv ./server/hsnmailenbeheer/settings_local_docker.py ./server/hsnmailenbeheer/settings_local.py

# Collect the static files for the admin GUI
RUN python ./server/manage.py collectstatic --noinput

# Build JavaScript libraries
RUN ./client/hsnmailenbeheer/generate.py source && \
    ./client/hsnmailenbeheer/generate.py build

FROM python:2.7-alpine

# Install required packages
RUN apk add --no-cache apache2 mariadb-dev openldap cups

# Copy the application from the builder
COPY --from=builder /app /app
COPY --from=builder "/usr/local/lib/python2.7/site-packages/mod_wsgi/server/mod_wsgi-py27.so" "/app/mod_wsgi-py27.so"
WORKDIR /app

# Link the Apache config
RUN ln -s /app/server/hsnmailenbeheer/hsnmailenbeheer_docker.conf /etc/apache2/conf.d/hsnmailenbeheer.conf

# Run the cups daemon and run the application through Apache
EXPOSE 80
ENTRYPOINT ["./run.sh"]
