# This Dockerfile expect build context to be the root of the repo!
ARG SERVICE_BASE_VER=1.8

# First, build the library
FROM apluslms/service-base:django-$SERVICE_BASE_VER as build

WORKDIR /src
COPY README.rst requirements.txt setup.py ./
COPY django_lti_login/ django_lti_login/

RUN python3 ./setup.py bdist_wheel -d /dist
RUN env PATH="$PATH:/install/bin" pip_install --prefix=/install /dist/*.whl

# clean stuff that is probably not needed.. NOTE: add languages back, when there is need for them
RUN find /install -type d -regex '.*/locale/[a-z_A-Z]+' -not -regex '.*/\(en\|fi\)' -print0 | xargs -0 rm -rf
RUN find /install -type d -name 'tests' -print0 | xargs -0 rm -rf

RUN for d in /install/lib/python*/; do mv "$d/site-packages" "$d/dist-packages"; done


# Second, create the actual service image with the lib
FROM apluslms/service-base:django-$SERVICE_BASE_VER

ENV CONTAINER_TYPE="lti-example"
WORKDIR /srv/lti/

COPY --from=build /install/lib /usr/local/lib
COPY example/ /srv/lti/

RUN : \
 && touch /etc/services.d/epmd/down /etc/services.d/rabbitmq/down \
 && echo '#!/bin/sh\n\
. /usr/local/lib/cont-init-functions.sh\n\
for d in /run/lti /local/lti /local/lti/static /local/lti/media; do\n\
  ensure_dir "$d" 2755 lti nogroup\n\
done\n\
echo "SECRET_KEY = \"$(head -c 512 /dev/urandom|sha256sum|cut -d" " -f1)\"" >> /srv/lti/exampleapp/settings.py\n\
' > /etc/cont-init.d/lti \
 && chmod -x /etc/cont-init.d/lti \
\
 && adduser --system --no-create-home --disabled-password --gecos "LTI webapp server,,," --home /srv/lti --ingroup nogroup lti \
 && chown -R lti.nogroup /srv/lti \
\
 && python3 -m compileall -q . \
 && echo '\n# Container changes\n\
STATIC_ROOT = "/local/lti/static/"\n\
DATABASES = {"default": {\n\
  "ENGINE": "django.db.backends.postgresql",\n\
  "NAME": "lti"}}\n\
' >> exampleapp/settings.py \
 && echo '#!/bin/sh -eu\n\
setuidgid $USER python3 manage.py add_lti_key -f -k testlti -d "test key"\n\
mkdir -p /data/aplus/lti-services-in/\n\
setuidgid $USER python3 manage.py export_for_aplus -k testlti -l "LTI Example" -i fire -b "http://$(hostname -i):8000" > /data/aplus/lti-services-in/lti-example.json\n\
' > /srv/lti-init.sh \
 && chmod +x /srv/lti-init.sh \
\
 && create-db.sh lti lti django-migrate.sh \
 && :

EXPOSE 8000
ENTRYPOINT [ "/init", "run-django.sh", "-u", "lti" ]
CMD [ "manage", "runserver", "0.0.0.0:8000" ]
