#!/bin/bash
docker run -d --rm --net=host -p 3000:3000 \
       -e PGRST_DB_URI="postgres://postgres:MiniPCP@192.168.15.69:5432/minipcp_lincevet" \
       -e PGRST_DB_ANON_ROLE="postgres" \
       postgrest/postgrest
