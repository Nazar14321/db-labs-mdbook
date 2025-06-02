# Проєктування бази даних

## Модель бізнес-об'єктів:

<center style="
   border-radius:4px;
   border: 1px solid #cfd7e6;
   box-shadow: 0 1px 3px 0 rgba(89,105,129,.05), 0 1px 1px 0 rgba(0,0,0,.025);
   padding: 1em;"
>

![General Diagram](https://www.plantuml.com/plantuml/png/PPBHZjKW48Rlvob8BpTBS_e6QzHuQtHzWB5Wn59eXgd6jzyp9NCAsniA__p_Ls1uAOp4-nh19mxyt_medg0i8Mr8k1h2j1I_cUbsQzIKdLTLWn-8mo-S-I5yoz43jDmnXNb9kFfEz2k6s2dRxyovLx2KVvaSGCSnrjcdkkKJPUn-YaepDdQY0Xk2_l1ZZX5_PaBE1Et23BVdfy5OicQOdgUXZ_N7_KAO68vHOxl63gSQltfQGoaX9pYdXx56QhZYDFFgSJsE8Jv1AraA9vdo7pypr2yhCohps8OCMY6jT3S00fN2D5WrAFhThyQsjvzycIbiB2U3rd2que9unRB0vJ6DXP7tqfeEHYSuZow69BV_BbUxgo8yubMN9NG4rTkjVFvxdtIBqI7xNY5VziZVMGeNnTWxj68qBo8zLAYwFXIdxMpxe9R-BTMzDbVTzb9cKZ-lvNp1mpJU9stmOXA2J2f2nhDIuTh35v_SliOt)

</center>

## ER-модель

<center style="
   border-radius:4px;
   border: 1px solid #cfd7e6;
   box-shadow: 0 1px 3px 0 rgba(89,105,129,.05), 0 1px 1px 0 rgba(0,0,0,.025);
   padding: 1em;"
>

   [![](https://img.plantuml.biz/plantuml/svg/ZLHDRzim3BtxLmW-3atHNerYQDOOHGxPXiu1TkLifjKYIu6aT1Ys_lTHb1tBZeib219IVEIZ-A5xvy7wOwko0zHxU4QHL-3s6z0ajwXzBlvacH0aIVyx6dC1JWI1J88-iYd4v-tcK_d4geOM2r6LtojMQulWfT4hy7IyMbPbjTwKR6eG6YKrdfdUifHpQRtSGUsPjrTcgUao_kWIyeOYUzcUHH-2hz3LLXv2XXm_qMSfci5-0GzzUwBobQj952pD1vyB8uH5TrJ-c-SoCMSIzy4e1J-C1MyiXqyFpZkKU7wrvYTsPUta_tOqSTywZ8H16Foss_KgUibwFva5R46gH3-0Sx-CRTAZ5-DD8TQRvMEPibK8RHmy4Yv9Cscao6-lFkHYiVWeyfiWzKCq1Trs89PumZF-ZLw3gQjM8Lx0TGWwlLiifl4fhyvyDGBm291nrAiaWG5KY0FQdR6j8tYez5ciD4RW2_L9C7pru7YotOnfkilGoWrlmBAkqRa7exqrAkTodwO6RIkTw_TbKEURGbL8LsMqUuyMkfLWAPgEbE6JKSZdGRZebPbRI-OQLtZIHmvFe7uJ9fKzcOSxJY6Sk2Z4S_WFBOe7iqHnN0Z3sjtVwsjA-nMLeGwJKMfwldIDNtOZYAUUANeetqT0qqejdOzt7C7UidlK3Jtl_m00)](https://editor.plantuml.com/uml/ZLHDRzim3BtxLmW-3atHNerYQDOOHGxPXiu1TkLifjKYIu6aT1Ys_lTHb1tBZeib219IVEIZ-A5xvy7wOwko0zHxU4QHL-3s6z0ajwXzBlvacH0aIVyx6dC1JWI1J88-iYd4v-tcK_d4geOM2r6LtojMQulWfT4hy7IyMbPbjTwKR6eG6YKrdfdUifHpQRtSGUsPjrTcgUao_kWIyeOYUzcUHH-2hz3LLXv2XXm_qMSfci5-0GzzUwBobQj952pD1vyB8uH5TrJ-c-SoCMSIzy4e1J-C1MyiXqyFpZkKU7wrvYTsPUta_tOqSTywZ8H16Foss_KgUibwFva5R46gH3-0Sx-CRTAZ5-DD8TQRvMEPibK8RHmy4Yv9Cscao6-lFkHYiVWeyfiWzKCq1Trs89PumZF-ZLw3gQjM8Lx0TGWwlLiifl4fhyvyDGBm291nrAiaWG5KY0FQdR6j8tYez5ciD4RW2_L9C7pru7YotOnfkilGoWrlmBAkqRa7exqrAkTodwO6RIkTw_TbKEURGbL8LsMqUuyMkfLWAPgEbE6JKSZdGRZebPbRI-OQLtZIHmvFe7uJ9fKzcOSxJY6Sk2Z4S_WFBOe7iqHnN0Z3sjtVwsjA-nMLeGwJKMfwldIDNtOZYAUUANeetqT0qqejdOzt7C7UidlK3Jtl_m00)


## Реляційна схема

![image](https://github.com/user-attachments/assets/504f3bd6-e090-42f3-8339-f8ead2826d13)

