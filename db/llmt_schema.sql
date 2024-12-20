PGDMP      ,                |            LLM-IT    16.4    16.0 �    +           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            ,           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            -           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            .           1262    34622    LLM-IT    DATABASE     s   CREATE DATABASE "LLM-IT" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
    DROP DATABASE "LLM-IT";
                postgres    false                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                azure_pg_admin    false            /           0    0 4   FUNCTION pg_replication_origin_advance(text, pg_lsn)    ACL     `   GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_advance(text, pg_lsn) TO azure_pg_admin;
       
   pg_catalog          azuresu    false    258            0           0    0 +   FUNCTION pg_replication_origin_create(text)    ACL     W   GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_create(text) TO azure_pg_admin;
       
   pg_catalog          azuresu    false    271            1           0    0 )   FUNCTION pg_replication_origin_drop(text)    ACL     U   GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_drop(text) TO azure_pg_admin;
       
   pg_catalog          azuresu    false    263            2           0    0 (   FUNCTION pg_replication_origin_oid(text)    ACL     T   GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_oid(text) TO azure_pg_admin;
       
   pg_catalog          azuresu    false    264            3           0    0 6   FUNCTION pg_replication_origin_progress(text, boolean)    ACL     b   GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_progress(text, boolean) TO azure_pg_admin;
       
   pg_catalog          azuresu    false    265            4           0    0 1   FUNCTION pg_replication_origin_session_is_setup()    ACL     ]   GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_session_is_setup() TO azure_pg_admin;
       
   pg_catalog          azuresu    false    266            5           0    0 8   FUNCTION pg_replication_origin_session_progress(boolean)    ACL     d   GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_session_progress(boolean) TO azure_pg_admin;
       
   pg_catalog          azuresu    false    267            6           0    0 .   FUNCTION pg_replication_origin_session_reset()    ACL     Z   GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_session_reset() TO azure_pg_admin;
       
   pg_catalog          azuresu    false    272            7           0    0 2   FUNCTION pg_replication_origin_session_setup(text)    ACL     ^   GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_session_setup(text) TO azure_pg_admin;
       
   pg_catalog          azuresu    false    268            8           0    0 +   FUNCTION pg_replication_origin_xact_reset()    ACL     W   GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_xact_reset() TO azure_pg_admin;
       
   pg_catalog          azuresu    false    269            9           0    0 K   FUNCTION pg_replication_origin_xact_setup(pg_lsn, timestamp with time zone)    ACL     w   GRANT ALL ON FUNCTION pg_catalog.pg_replication_origin_xact_setup(pg_lsn, timestamp with time zone) TO azure_pg_admin;
       
   pg_catalog          azuresu    false    270            :           0    0    FUNCTION pg_show_replication_origin_status(OUT local_id oid, OUT external_id text, OUT remote_lsn pg_lsn, OUT local_lsn pg_lsn)    ACL     �   GRANT ALL ON FUNCTION pg_catalog.pg_show_replication_origin_status(OUT local_id oid, OUT external_id text, OUT remote_lsn pg_lsn, OUT local_lsn pg_lsn) TO azure_pg_admin;
       
   pg_catalog          azuresu    false    273            ;           0    0    FUNCTION pg_stat_reset()    ACL     D   GRANT ALL ON FUNCTION pg_catalog.pg_stat_reset() TO azure_pg_admin;
       
   pg_catalog          azuresu    false    259            <           0    0 #   FUNCTION pg_stat_reset_shared(text)    ACL     O   GRANT ALL ON FUNCTION pg_catalog.pg_stat_reset_shared(text) TO azure_pg_admin;
       
   pg_catalog          azuresu    false    260            =           0    0 4   FUNCTION pg_stat_reset_single_function_counters(oid)    ACL     `   GRANT ALL ON FUNCTION pg_catalog.pg_stat_reset_single_function_counters(oid) TO azure_pg_admin;
       
   pg_catalog          azuresu    false    262            >           0    0 1   FUNCTION pg_stat_reset_single_table_counters(oid)    ACL     ]   GRANT ALL ON FUNCTION pg_catalog.pg_stat_reset_single_table_counters(oid) TO azure_pg_admin;
       
   pg_catalog          azuresu    false    261            ?           0    0    COLUMN pg_config.name    ACL     D   GRANT SELECT(name) ON TABLE pg_catalog.pg_config TO azure_pg_admin;
       
   pg_catalog          azuresu    false    98            @           0    0    COLUMN pg_config.setting    ACL     G   GRANT SELECT(setting) ON TABLE pg_catalog.pg_config TO azure_pg_admin;
       
   pg_catalog          azuresu    false    98            A           0    0 $   COLUMN pg_hba_file_rules.line_number    ACL     S   GRANT SELECT(line_number) ON TABLE pg_catalog.pg_hba_file_rules TO azure_pg_admin;
       
   pg_catalog          azuresu    false    94            B           0    0    COLUMN pg_hba_file_rules.type    ACL     L   GRANT SELECT(type) ON TABLE pg_catalog.pg_hba_file_rules TO azure_pg_admin;
       
   pg_catalog          azuresu    false    94            C           0    0 !   COLUMN pg_hba_file_rules.database    ACL     P   GRANT SELECT(database) ON TABLE pg_catalog.pg_hba_file_rules TO azure_pg_admin;
       
   pg_catalog          azuresu    false    94            D           0    0 "   COLUMN pg_hba_file_rules.user_name    ACL     Q   GRANT SELECT(user_name) ON TABLE pg_catalog.pg_hba_file_rules TO azure_pg_admin;
       
   pg_catalog          azuresu    false    94            E           0    0     COLUMN pg_hba_file_rules.address    ACL     O   GRANT SELECT(address) ON TABLE pg_catalog.pg_hba_file_rules TO azure_pg_admin;
       
   pg_catalog          azuresu    false    94            F           0    0     COLUMN pg_hba_file_rules.netmask    ACL     O   GRANT SELECT(netmask) ON TABLE pg_catalog.pg_hba_file_rules TO azure_pg_admin;
       
   pg_catalog          azuresu    false    94            G           0    0 $   COLUMN pg_hba_file_rules.auth_method    ACL     S   GRANT SELECT(auth_method) ON TABLE pg_catalog.pg_hba_file_rules TO azure_pg_admin;
       
   pg_catalog          azuresu    false    94            H           0    0     COLUMN pg_hba_file_rules.options    ACL     O   GRANT SELECT(options) ON TABLE pg_catalog.pg_hba_file_rules TO azure_pg_admin;
       
   pg_catalog          azuresu    false    94            I           0    0    COLUMN pg_hba_file_rules.error    ACL     M   GRANT SELECT(error) ON TABLE pg_catalog.pg_hba_file_rules TO azure_pg_admin;
       
   pg_catalog          azuresu    false    94            J           0    0 ,   COLUMN pg_replication_origin_status.local_id    ACL     [   GRANT SELECT(local_id) ON TABLE pg_catalog.pg_replication_origin_status TO azure_pg_admin;
       
   pg_catalog          azuresu    false    144            K           0    0 /   COLUMN pg_replication_origin_status.external_id    ACL     ^   GRANT SELECT(external_id) ON TABLE pg_catalog.pg_replication_origin_status TO azure_pg_admin;
       
   pg_catalog          azuresu    false    144            L           0    0 .   COLUMN pg_replication_origin_status.remote_lsn    ACL     ]   GRANT SELECT(remote_lsn) ON TABLE pg_catalog.pg_replication_origin_status TO azure_pg_admin;
       
   pg_catalog          azuresu    false    144            M           0    0 -   COLUMN pg_replication_origin_status.local_lsn    ACL     \   GRANT SELECT(local_lsn) ON TABLE pg_catalog.pg_replication_origin_status TO azure_pg_admin;
       
   pg_catalog          azuresu    false    144            N           0    0     COLUMN pg_shmem_allocations.name    ACL     O   GRANT SELECT(name) ON TABLE pg_catalog.pg_shmem_allocations TO azure_pg_admin;
       
   pg_catalog          azuresu    false    99            O           0    0    COLUMN pg_shmem_allocations.off    ACL     N   GRANT SELECT(off) ON TABLE pg_catalog.pg_shmem_allocations TO azure_pg_admin;
       
   pg_catalog          azuresu    false    99            P           0    0     COLUMN pg_shmem_allocations.size    ACL     O   GRANT SELECT(size) ON TABLE pg_catalog.pg_shmem_allocations TO azure_pg_admin;
       
   pg_catalog          azuresu    false    99            Q           0    0 *   COLUMN pg_shmem_allocations.allocated_size    ACL     Y   GRANT SELECT(allocated_size) ON TABLE pg_catalog.pg_shmem_allocations TO azure_pg_admin;
       
   pg_catalog          azuresu    false    99            R           0    0    COLUMN pg_statistic.starelid    ACL     K   GRANT SELECT(starelid) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            S           0    0    COLUMN pg_statistic.staattnum    ACL     L   GRANT SELECT(staattnum) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            T           0    0    COLUMN pg_statistic.stainherit    ACL     M   GRANT SELECT(stainherit) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            U           0    0    COLUMN pg_statistic.stanullfrac    ACL     N   GRANT SELECT(stanullfrac) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            V           0    0    COLUMN pg_statistic.stawidth    ACL     K   GRANT SELECT(stawidth) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            W           0    0    COLUMN pg_statistic.stadistinct    ACL     N   GRANT SELECT(stadistinct) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            X           0    0    COLUMN pg_statistic.stakind1    ACL     K   GRANT SELECT(stakind1) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            Y           0    0    COLUMN pg_statistic.stakind2    ACL     K   GRANT SELECT(stakind2) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            Z           0    0    COLUMN pg_statistic.stakind3    ACL     K   GRANT SELECT(stakind3) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            [           0    0    COLUMN pg_statistic.stakind4    ACL     K   GRANT SELECT(stakind4) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            \           0    0    COLUMN pg_statistic.stakind5    ACL     K   GRANT SELECT(stakind5) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            ]           0    0    COLUMN pg_statistic.staop1    ACL     I   GRANT SELECT(staop1) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            ^           0    0    COLUMN pg_statistic.staop2    ACL     I   GRANT SELECT(staop2) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            _           0    0    COLUMN pg_statistic.staop3    ACL     I   GRANT SELECT(staop3) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            `           0    0    COLUMN pg_statistic.staop4    ACL     I   GRANT SELECT(staop4) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            a           0    0    COLUMN pg_statistic.staop5    ACL     I   GRANT SELECT(staop5) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            b           0    0    COLUMN pg_statistic.stacoll1    ACL     K   GRANT SELECT(stacoll1) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            c           0    0    COLUMN pg_statistic.stacoll2    ACL     K   GRANT SELECT(stacoll2) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            d           0    0    COLUMN pg_statistic.stacoll3    ACL     K   GRANT SELECT(stacoll3) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            e           0    0    COLUMN pg_statistic.stacoll4    ACL     K   GRANT SELECT(stacoll4) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            f           0    0    COLUMN pg_statistic.stacoll5    ACL     K   GRANT SELECT(stacoll5) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            g           0    0    COLUMN pg_statistic.stanumbers1    ACL     N   GRANT SELECT(stanumbers1) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            h           0    0    COLUMN pg_statistic.stanumbers2    ACL     N   GRANT SELECT(stanumbers2) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            i           0    0    COLUMN pg_statistic.stanumbers3    ACL     N   GRANT SELECT(stanumbers3) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            j           0    0    COLUMN pg_statistic.stanumbers4    ACL     N   GRANT SELECT(stanumbers4) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            k           0    0    COLUMN pg_statistic.stanumbers5    ACL     N   GRANT SELECT(stanumbers5) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            l           0    0    COLUMN pg_statistic.stavalues1    ACL     M   GRANT SELECT(stavalues1) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            m           0    0    COLUMN pg_statistic.stavalues2    ACL     M   GRANT SELECT(stavalues2) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            n           0    0    COLUMN pg_statistic.stavalues3    ACL     M   GRANT SELECT(stavalues3) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            o           0    0    COLUMN pg_statistic.stavalues4    ACL     M   GRANT SELECT(stavalues4) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            p           0    0    COLUMN pg_statistic.stavalues5    ACL     M   GRANT SELECT(stavalues5) ON TABLE pg_catalog.pg_statistic TO azure_pg_admin;
       
   pg_catalog          azuresu    false    39            q           0    0    COLUMN pg_subscription.oid    ACL     I   GRANT SELECT(oid) ON TABLE pg_catalog.pg_subscription TO azure_pg_admin;
       
   pg_catalog          azuresu    false    64            r           0    0    COLUMN pg_subscription.subdbid    ACL     M   GRANT SELECT(subdbid) ON TABLE pg_catalog.pg_subscription TO azure_pg_admin;
       
   pg_catalog          azuresu    false    64            s           0    0    COLUMN pg_subscription.subname    ACL     M   GRANT SELECT(subname) ON TABLE pg_catalog.pg_subscription TO azure_pg_admin;
       
   pg_catalog          azuresu    false    64            t           0    0    COLUMN pg_subscription.subowner    ACL     N   GRANT SELECT(subowner) ON TABLE pg_catalog.pg_subscription TO azure_pg_admin;
       
   pg_catalog          azuresu    false    64            u           0    0 !   COLUMN pg_subscription.subenabled    ACL     P   GRANT SELECT(subenabled) ON TABLE pg_catalog.pg_subscription TO azure_pg_admin;
       
   pg_catalog          azuresu    false    64            v           0    0 "   COLUMN pg_subscription.subconninfo    ACL     Q   GRANT SELECT(subconninfo) ON TABLE pg_catalog.pg_subscription TO azure_pg_admin;
       
   pg_catalog          azuresu    false    64            w           0    0 "   COLUMN pg_subscription.subslotname    ACL     Q   GRANT SELECT(subslotname) ON TABLE pg_catalog.pg_subscription TO azure_pg_admin;
       
   pg_catalog          azuresu    false    64            x           0    0 $   COLUMN pg_subscription.subsynccommit    ACL     S   GRANT SELECT(subsynccommit) ON TABLE pg_catalog.pg_subscription TO azure_pg_admin;
       
   pg_catalog          azuresu    false    64            y           0    0 &   COLUMN pg_subscription.subpublications    ACL     U   GRANT SELECT(subpublications) ON TABLE pg_catalog.pg_subscription TO azure_pg_admin;
       
   pg_catalog          azuresu    false    64            �            1259    124421    ORG_PEP_info    TABLE     o   CREATE TABLE public."ORG_PEP_info" (
    business_license_no integer NOT NULL,
    high_risk_factor boolean
);
 "   DROP TABLE public."ORG_PEP_info";
       public         heap    postgres    false    5            �            1259    124420 $   ORG_PEP_info_business_license_no_seq    SEQUENCE     �   CREATE SEQUENCE public."ORG_PEP_info_business_license_no_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 =   DROP SEQUENCE public."ORG_PEP_info_business_license_no_seq";
       public          postgres    false    245    5            z           0    0 $   ORG_PEP_info_business_license_no_seq    SEQUENCE OWNED BY     q   ALTER SEQUENCE public."ORG_PEP_info_business_license_no_seq" OWNED BY public."ORG_PEP_info".business_license_no;
          public          postgres    false    244            �            1259    138138    PEP_data    TABLE     �   CREATE TABLE public."PEP_data" (
    ssn_no bigint NOT NULL,
    passport_no character varying(10),
    politically_exposed boolean,
    pep_user_input boolean,
    bank_acc_no bigint,
    credit_score integer
);
    DROP TABLE public."PEP_data";
       public         heap    postgres    false    5            �            1259    138137    PEP_data_ssn_no_seq    SEQUENCE     ~   CREATE SEQUENCE public."PEP_data_ssn_no_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public."PEP_data_ssn_no_seq";
       public          postgres    false    251    5            {           0    0    PEP_data_ssn_no_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public."PEP_data_ssn_no_seq" OWNED BY public."PEP_data".ssn_no;
          public          postgres    false    250            �            1259    121258    PEP_info    TABLE     �   CREATE TABLE public."PEP_info" (
    ssn_no integer NOT NULL,
    passport_no character varying,
    politically_exposed boolean
);
    DROP TABLE public."PEP_info";
       public         heap    postgres    false    5            �            1259    121257    PEP_info_ssn_no_seq    SEQUENCE     �   CREATE SEQUENCE public."PEP_info_ssn_no_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public."PEP_info_ssn_no_seq";
       public          postgres    false    5    239            |           0    0    PEP_info_ssn_no_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public."PEP_info_ssn_no_seq" OWNED BY public."PEP_info".ssn_no;
          public          postgres    false    238            �            1259    124026    chat_history    TABLE       CREATE TABLE public.chat_history (
    id integer NOT NULL,
    ai_question character varying,
    human_answer character varying,
    stepper character varying,
    "timestamp" character varying,
    conversation_type character varying,
    thread_id character varying
);
     DROP TABLE public.chat_history;
       public         heap    postgres    false    5            �            1259    124025    chat_history_id_seq    SEQUENCE     �   CREATE SEQUENCE public.chat_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.chat_history_id_seq;
       public          postgres    false    243    5            }           0    0    chat_history_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.chat_history_id_seq OWNED BY public.chat_history.id;
          public          postgres    false    242            �            1259    41836    checkpoint_blobs    TABLE     �   CREATE TABLE public.checkpoint_blobs (
    thread_id text NOT NULL,
    checkpoint_ns text DEFAULT ''::text NOT NULL,
    channel text NOT NULL,
    version text NOT NULL,
    type text NOT NULL,
    blob bytea
);
 $   DROP TABLE public.checkpoint_blobs;
       public         heap    postgres    false    5            �            1259    41822    checkpoint_migrations    TABLE     F   CREATE TABLE public.checkpoint_migrations (
    v integer NOT NULL
);
 )   DROP TABLE public.checkpoint_migrations;
       public         heap    postgres    false    5            �            1259    41844    checkpoint_writes    TABLE       CREATE TABLE public.checkpoint_writes (
    thread_id text NOT NULL,
    checkpoint_ns text DEFAULT ''::text NOT NULL,
    checkpoint_id text NOT NULL,
    task_id text NOT NULL,
    idx integer NOT NULL,
    channel text NOT NULL,
    type text,
    blob bytea NOT NULL
);
 %   DROP TABLE public.checkpoint_writes;
       public         heap    postgres    false    5            �            1259    41827    checkpoints    TABLE     X  CREATE TABLE public.checkpoints (
    thread_id text NOT NULL,
    checkpoint_ns text DEFAULT ''::text NOT NULL,
    checkpoint_id text NOT NULL,
    parent_checkpoint_id text,
    type text,
    checkpoint jsonb NOT NULL,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.checkpoints;
       public         heap    postgres    false    5            �            1259    42665    conversation_state    TABLE     �   CREATE TABLE public.conversation_state (
    uuid character varying NOT NULL,
    thread_id character varying,
    state_obj json
);
 &   DROP TABLE public.conversation_state;
       public         heap    postgres    false    5            �            1259    120959    conversations    TABLE     g   CREATE TABLE public.conversations (
    thread_id character varying(255) NOT NULL,
    sas_url text
);
 !   DROP TABLE public.conversations;
       public         heap    postgres    false    5            �            1259    42610    country_specific_info    TABLE     �   CREATE TABLE public.country_specific_info (
    country_name character varying(25) NOT NULL,
    guidelines character varying,
    is_aadhar boolean,
    is_passport boolean,
    is_ssn boolean,
    is_dl boolean
);
 )   DROP TABLE public.country_specific_info;
       public         heap    postgres    false    5            �            1259    42617    doc_table_aadhar    TABLE     �   CREATE TABLE public.doc_table_aadhar (
    uuid character varying NOT NULL,
    first_name character varying(25),
    last_name character varying(25),
    dob date,
    aadhar_no integer,
    address character varying(255),
    aadhar_binary bytea
);
 $   DROP TABLE public.doc_table_aadhar;
       public         heap    postgres    false    5            �            1259    42641    doc_table_dl    TABLE       CREATE TABLE public.doc_table_dl (
    uuid character varying NOT NULL,
    first_name character varying(25),
    last_name character varying(25),
    dob date,
    sex character varying(10),
    date_of_issue date,
    date_of_expiry date,
    dl_no character varying(30)
);
     DROP TABLE public.doc_table_dl;
       public         heap    postgres    false    5            �            1259    42653    doc_table_passport    TABLE     (  CREATE TABLE public.doc_table_passport (
    uuid character varying NOT NULL,
    first_name character varying(25),
    last_name character varying(25),
    date_of_issue date,
    date_of_expiry date,
    dob date,
    passport_no character varying(30),
    nationality character varying(25)
);
 &   DROP TABLE public.doc_table_passport;
       public         heap    postgres    false    5            �            1259    42629    doc_table_ssn    TABLE     �   CREATE TABLE public.doc_table_ssn (
    uuid character varying NOT NULL,
    first_name character varying(25),
    last_name character varying(25),
    ssn_no integer
);
 !   DROP TABLE public.doc_table_ssn;
       public         heap    postgres    false    5            �            1259    135932    document_extracted_data    TABLE     '  CREATE TABLE public.document_extracted_data (
    id integer NOT NULL,
    document_type character varying(255),
    firstname character varying(255),
    lastname character varying(100),
    document_number character varying(255),
    gender character varying(255),
    date_of_birth character varying(255),
    date_of_issue character varying(255),
    date_of_expiration character varying(255),
    place_of_birth character varying(255),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    thread_id character varying(255)
);
 +   DROP TABLE public.document_extracted_data;
       public         heap    postgres    false    5            �            1259    135931    document_extracted_data_id_seq    SEQUENCE     �   CREATE SEQUENCE public.document_extracted_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.document_extracted_data_id_seq;
       public          postgres    false    5    249            ~           0    0    document_extracted_data_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.document_extracted_data_id_seq OWNED BY public.document_extracted_data.id;
          public          postgres    false    248                       1259    138966 
   guidelines    TABLE     �   CREATE TABLE public.guidelines (
    id integer NOT NULL,
    usa_individual_guideline character varying(2555) NOT NULL,
    usa_organization_guideline character varying(2555) NOT NULL
);
    DROP TABLE public.guidelines;
       public         heap    postgres    false    5                        1259    138965    guidelines_id_seq    SEQUENCE     �   CREATE SEQUENCE public.guidelines_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.guidelines_id_seq;
       public          postgres    false    257    5                       0    0    guidelines_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.guidelines_id_seq OWNED BY public.guidelines.id;
          public          postgres    false    256            �            1259    119755    jsonencrypted    TABLE     �   CREATE TABLE public.jsonencrypted (
    id integer NOT NULL,
    encrypted_json character varying,
    private_key character varying,
    iv character varying
);
 !   DROP TABLE public.jsonencrypted;
       public         heap    postgres    false    5            �            1259    119754    jsonencrypted_id_seq    SEQUENCE     �   CREATE SEQUENCE public.jsonencrypted_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.jsonencrypted_id_seq;
       public          postgres    false    5    229            �           0    0    jsonencrypted_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.jsonencrypted_id_seq OWNED BY public.jsonencrypted.id;
          public          postgres    false    228            �            1259    120966    messages    TABLE     �   CREATE TABLE public.messages (
    id character varying(255) NOT NULL,
    ai_question text,
    human_answer text,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    thread_id character varying(255)
);
    DROP TABLE public.messages;
       public         heap    postgres    false    5            �            1259    138276    org_pep    TABLE     �   CREATE TABLE public.org_pep (
    id integer NOT NULL,
    business_license_no integer,
    high_risk_factor boolean,
    annual_revenue character varying,
    pep_members boolean,
    dividends_pq character varying
);
    DROP TABLE public.org_pep;
       public         heap    postgres    false    5            �            1259    138275    org_pep_id_seq    SEQUENCE     �   CREATE SEQUENCE public.org_pep_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.org_pep_id_seq;
       public          postgres    false    255    5            �           0    0    org_pep_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.org_pep_id_seq OWNED BY public.org_pep.id;
          public          postgres    false    254            �            1259    123912    past_records    TABLE     !  CREATE TABLE public.past_records (
    id integer NOT NULL,
    name character varying(255),
    thread_id character varying(255),
    type character varying(50),
    kyc_status character varying(50),
    date_added timestamp without time zone,
    explaination character varying(3000)
);
     DROP TABLE public.past_records;
       public         heap    postgres    false    5            �            1259    123911    past_records_id_seq    SEQUENCE     �   CREATE SEQUENCE public.past_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.past_records_id_seq;
       public          postgres    false    241    5            �           0    0    past_records_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.past_records_id_seq OWNED BY public.past_records.id;
          public          postgres    false    240            �            1259    120980    roles    TABLE     b   CREATE TABLE public.roles (
    role_id integer NOT NULL,
    role_name character varying(255)
);
    DROP TABLE public.roles;
       public         heap    postgres    false    5            �            1259    120979    roles_role_id_seq    SEQUENCE     �   CREATE SEQUENCE public.roles_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.roles_role_id_seq;
       public          postgres    false    233    5            �           0    0    roles_role_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.roles_role_id_seq OWNED BY public.roles.role_id;
          public          postgres    false    232            �            1259    138238    sastoken    TABLE     �   CREATE TABLE public.sastoken (
    id integer NOT NULL,
    file_name character varying,
    sas_token character varying,
    creation_time character varying
);
    DROP TABLE public.sastoken;
       public         heap    postgres    false    5            �            1259    138237    sastoken_id_seq    SEQUENCE     �   CREATE SEQUENCE public.sastoken_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.sastoken_id_seq;
       public          postgres    false    253    5            �           0    0    sastoken_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.sastoken_id_seq OWNED BY public.sastoken.id;
          public          postgres    false    252            �            1259    121183    steps    TABLE     �   CREATE TABLE public.steps (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    icon character varying(50) NOT NULL,
    completed boolean DEFAULT false NOT NULL
);
    DROP TABLE public.steps;
       public         heap    postgres    false    5            �            1259    121182    steps_id_seq    SEQUENCE     �   CREATE SEQUENCE public.steps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.steps_id_seq;
       public          postgres    false    5    237            �           0    0    steps_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.steps_id_seq OWNED BY public.steps.id;
          public          postgres    false    236            �            1259    135910    user_extracted_data    TABLE     m  CREATE TABLE public.user_extracted_data (
    id integer NOT NULL,
    country character varying(255),
    firstname character varying(255),
    lastname character varying(100),
    father_fullname character varying(255),
    gender character varying(255),
    date_of_birth character varying(255),
    marital_status character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    thread_id character varying(255),
    document_number character varying(255),
    issue_date character varying(255),
    expiration_date character varying(255),
    place_of_birth character varying(255)
);
 '   DROP TABLE public.user_extracted_data;
       public         heap    postgres    false    5            �            1259    135909    user_extracted_data_id_seq    SEQUENCE     �   CREATE SEQUENCE public.user_extracted_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.user_extracted_data_id_seq;
       public          postgres    false    247    5            �           0    0    user_extracted_data_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.user_extracted_data_id_seq OWNED BY public.user_extracted_data.id;
          public          postgres    false    246            �            1259    42603 	   user_info    TABLE     [  CREATE TABLE public.user_info (
    uuid character varying NOT NULL,
    first_name character varying(25),
    last_name character varying(25),
    father_name character varying(50),
    ssn_no integer,
    gender character varying(10),
    marital_status character varying(20),
    ssn_bool boolean,
    aadhar_no integer,
    aadhar_bool boolean,
    dl character varying(20),
    dl_bool boolean,
    passport_no character varying(20),
    passport_bool boolean,
    passport_link character varying,
    ssn_link character varying,
    dl_link character varying,
    aadhar_link character varying
);
    DROP TABLE public.user_info;
       public         heap    postgres    false    5            �            1259    119648 
   user_state    TABLE     q   CREATE TABLE public.user_state (
    id integer NOT NULL,
    thread_id character varying,
    state_obj json
);
    DROP TABLE public.user_state;
       public         heap    postgres    false    5            �            1259    119647    user_state_id_seq    SEQUENCE     �   CREATE SEQUENCE public.user_state_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.user_state_id_seq;
       public          postgres    false    227    5            �           0    0    user_state_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.user_state_id_seq OWNED BY public.user_state.id;
          public          postgres    false    226            �            1259    121020    users    TABLE     �  CREATE TABLE public.users (
    user_id integer NOT NULL,
    email_id character varying(255),
    username character varying(255) NOT NULL,
    last_login_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    created_on timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    password character varying(255),
    role_id integer NOT NULL,
    firstname character varying(255) NOT NULL,
    lastname character varying(255) NOT NULL,
    ohr_id character varying(255) NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false    5            �            1259    121019    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public          postgres    false    5    235            �           0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public          postgres    false    234            P           2604    124424     ORG_PEP_info business_license_no    DEFAULT     �   ALTER TABLE ONLY public."ORG_PEP_info" ALTER COLUMN business_license_no SET DEFAULT nextval('public."ORG_PEP_info_business_license_no_seq"'::regclass);
 Q   ALTER TABLE public."ORG_PEP_info" ALTER COLUMN business_license_no DROP DEFAULT;
       public          postgres    false    245    244    245            U           2604    138141    PEP_data ssn_no    DEFAULT     v   ALTER TABLE ONLY public."PEP_data" ALTER COLUMN ssn_no SET DEFAULT nextval('public."PEP_data_ssn_no_seq"'::regclass);
 @   ALTER TABLE public."PEP_data" ALTER COLUMN ssn_no DROP DEFAULT;
       public          postgres    false    250    251    251            M           2604    121261    PEP_info ssn_no    DEFAULT     v   ALTER TABLE ONLY public."PEP_info" ALTER COLUMN ssn_no SET DEFAULT nextval('public."PEP_info_ssn_no_seq"'::regclass);
 @   ALTER TABLE public."PEP_info" ALTER COLUMN ssn_no DROP DEFAULT;
       public          postgres    false    239    238    239            O           2604    124029    chat_history id    DEFAULT     r   ALTER TABLE ONLY public.chat_history ALTER COLUMN id SET DEFAULT nextval('public.chat_history_id_seq'::regclass);
 >   ALTER TABLE public.chat_history ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    243    242    243            S           2604    135935    document_extracted_data id    DEFAULT     �   ALTER TABLE ONLY public.document_extracted_data ALTER COLUMN id SET DEFAULT nextval('public.document_extracted_data_id_seq'::regclass);
 I   ALTER TABLE public.document_extracted_data ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    249    248    249            X           2604    138969    guidelines id    DEFAULT     n   ALTER TABLE ONLY public.guidelines ALTER COLUMN id SET DEFAULT nextval('public.guidelines_id_seq'::regclass);
 <   ALTER TABLE public.guidelines ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    256    257    257            E           2604    119758    jsonencrypted id    DEFAULT     t   ALTER TABLE ONLY public.jsonencrypted ALTER COLUMN id SET DEFAULT nextval('public.jsonencrypted_id_seq'::regclass);
 ?   ALTER TABLE public.jsonencrypted ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    229    228    229            W           2604    138279 
   org_pep id    DEFAULT     h   ALTER TABLE ONLY public.org_pep ALTER COLUMN id SET DEFAULT nextval('public.org_pep_id_seq'::regclass);
 9   ALTER TABLE public.org_pep ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    255    254    255            N           2604    123915    past_records id    DEFAULT     r   ALTER TABLE ONLY public.past_records ALTER COLUMN id SET DEFAULT nextval('public.past_records_id_seq'::regclass);
 >   ALTER TABLE public.past_records ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    240    241    241            G           2604    120983    roles role_id    DEFAULT     n   ALTER TABLE ONLY public.roles ALTER COLUMN role_id SET DEFAULT nextval('public.roles_role_id_seq'::regclass);
 <   ALTER TABLE public.roles ALTER COLUMN role_id DROP DEFAULT;
       public          postgres    false    232    233    233            V           2604    138241    sastoken id    DEFAULT     j   ALTER TABLE ONLY public.sastoken ALTER COLUMN id SET DEFAULT nextval('public.sastoken_id_seq'::regclass);
 :   ALTER TABLE public.sastoken ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    252    253    253            K           2604    121186    steps id    DEFAULT     d   ALTER TABLE ONLY public.steps ALTER COLUMN id SET DEFAULT nextval('public.steps_id_seq'::regclass);
 7   ALTER TABLE public.steps ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    237    236    237            Q           2604    135913    user_extracted_data id    DEFAULT     �   ALTER TABLE ONLY public.user_extracted_data ALTER COLUMN id SET DEFAULT nextval('public.user_extracted_data_id_seq'::regclass);
 E   ALTER TABLE public.user_extracted_data ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    246    247    247            D           2604    119651    user_state id    DEFAULT     n   ALTER TABLE ONLY public.user_state ALTER COLUMN id SET DEFAULT nextval('public.user_state_id_seq'::regclass);
 <   ALTER TABLE public.user_state ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    227    226    227            H           2604    121023    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    235    234    235            �           2606    124426    ORG_PEP_info ORG_PEP_info_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY public."ORG_PEP_info"
    ADD CONSTRAINT "ORG_PEP_info_pkey" PRIMARY KEY (business_license_no);
 L   ALTER TABLE ONLY public."ORG_PEP_info" DROP CONSTRAINT "ORG_PEP_info_pkey";
       public            postgres    false    245            �           2606    138143    PEP_data PEP_data_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public."PEP_data"
    ADD CONSTRAINT "PEP_data_pkey" PRIMARY KEY (ssn_no);
 D   ALTER TABLE ONLY public."PEP_data" DROP CONSTRAINT "PEP_data_pkey";
       public            postgres    false    251            ~           2606    121265    PEP_info PEP_info_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public."PEP_info"
    ADD CONSTRAINT "PEP_info_pkey" PRIMARY KEY (ssn_no);
 D   ALTER TABLE ONLY public."PEP_info" DROP CONSTRAINT "PEP_info_pkey";
       public            postgres    false    239            �           2606    124033    chat_history chat_history_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.chat_history
    ADD CONSTRAINT chat_history_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.chat_history DROP CONSTRAINT chat_history_pkey;
       public            postgres    false    243            ^           2606    41843 &   checkpoint_blobs checkpoint_blobs_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.checkpoint_blobs
    ADD CONSTRAINT checkpoint_blobs_pkey PRIMARY KEY (thread_id, checkpoint_ns, channel, version);
 P   ALTER TABLE ONLY public.checkpoint_blobs DROP CONSTRAINT checkpoint_blobs_pkey;
       public            postgres    false    217    217    217    217            Z           2606    41826 0   checkpoint_migrations checkpoint_migrations_pkey 
   CONSTRAINT     m   ALTER TABLE ONLY public.checkpoint_migrations
    ADD CONSTRAINT checkpoint_migrations_pkey PRIMARY KEY (v);
 Z   ALTER TABLE ONLY public.checkpoint_migrations DROP CONSTRAINT checkpoint_migrations_pkey;
       public            postgres    false    215            `           2606    41851 (   checkpoint_writes checkpoint_writes_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.checkpoint_writes
    ADD CONSTRAINT checkpoint_writes_pkey PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx);
 R   ALTER TABLE ONLY public.checkpoint_writes DROP CONSTRAINT checkpoint_writes_pkey;
       public            postgres    false    218    218    218    218    218            \           2606    41835    checkpoints checkpoints_pkey 
   CONSTRAINT        ALTER TABLE ONLY public.checkpoints
    ADD CONSTRAINT checkpoints_pkey PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id);
 F   ALTER TABLE ONLY public.checkpoints DROP CONSTRAINT checkpoints_pkey;
       public            postgres    false    216    216    216            n           2606    42671 *   conversation_state conversation_state_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.conversation_state
    ADD CONSTRAINT conversation_state_pkey PRIMARY KEY (uuid);
 T   ALTER TABLE ONLY public.conversation_state DROP CONSTRAINT conversation_state_pkey;
       public            postgres    false    225            t           2606    120965     conversations conversations_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_pkey PRIMARY KEY (thread_id);
 J   ALTER TABLE ONLY public.conversations DROP CONSTRAINT conversations_pkey;
       public            postgres    false    230            d           2606    42616 0   country_specific_info country_specific_info_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.country_specific_info
    ADD CONSTRAINT country_specific_info_pkey PRIMARY KEY (country_name);
 Z   ALTER TABLE ONLY public.country_specific_info DROP CONSTRAINT country_specific_info_pkey;
       public            postgres    false    220            f           2606    42623 &   doc_table_aadhar doc_table_aadhar_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.doc_table_aadhar
    ADD CONSTRAINT doc_table_aadhar_pkey PRIMARY KEY (uuid);
 P   ALTER TABLE ONLY public.doc_table_aadhar DROP CONSTRAINT doc_table_aadhar_pkey;
       public            postgres    false    221            j           2606    42647    doc_table_dl doc_table_dl_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.doc_table_dl
    ADD CONSTRAINT doc_table_dl_pkey PRIMARY KEY (uuid);
 H   ALTER TABLE ONLY public.doc_table_dl DROP CONSTRAINT doc_table_dl_pkey;
       public            postgres    false    223            l           2606    42659 *   doc_table_passport doc_table_passport_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.doc_table_passport
    ADD CONSTRAINT doc_table_passport_pkey PRIMARY KEY (uuid);
 T   ALTER TABLE ONLY public.doc_table_passport DROP CONSTRAINT doc_table_passport_pkey;
       public            postgres    false    224            h           2606    42635     doc_table_ssn doc_table_ssn_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.doc_table_ssn
    ADD CONSTRAINT doc_table_ssn_pkey PRIMARY KEY (uuid);
 J   ALTER TABLE ONLY public.doc_table_ssn DROP CONSTRAINT doc_table_ssn_pkey;
       public            postgres    false    222            �           2606    135940 4   document_extracted_data document_extracted_data_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.document_extracted_data
    ADD CONSTRAINT document_extracted_data_pkey PRIMARY KEY (id);
 ^   ALTER TABLE ONLY public.document_extracted_data DROP CONSTRAINT document_extracted_data_pkey;
       public            postgres    false    249            �           2606    138973    guidelines guidelines_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.guidelines
    ADD CONSTRAINT guidelines_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.guidelines DROP CONSTRAINT guidelines_pkey;
       public            postgres    false    257            r           2606    119762     jsonencrypted jsonencrypted_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.jsonencrypted
    ADD CONSTRAINT jsonencrypted_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.jsonencrypted DROP CONSTRAINT jsonencrypted_pkey;
       public            postgres    false    229            v           2606    120973    messages messages_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_pkey;
       public            postgres    false    231            �           2606    138285 '   org_pep org_pep_business_license_no_key 
   CONSTRAINT     q   ALTER TABLE ONLY public.org_pep
    ADD CONSTRAINT org_pep_business_license_no_key UNIQUE (business_license_no);
 Q   ALTER TABLE ONLY public.org_pep DROP CONSTRAINT org_pep_business_license_no_key;
       public            postgres    false    255            �           2606    138283    org_pep org_pep_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.org_pep
    ADD CONSTRAINT org_pep_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.org_pep DROP CONSTRAINT org_pep_pkey;
       public            postgres    false    255            �           2606    123919    past_records past_records_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.past_records
    ADD CONSTRAINT past_records_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.past_records DROP CONSTRAINT past_records_pkey;
       public            postgres    false    241            x           2606    120985    roles roles_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);
 :   ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_pkey;
       public            postgres    false    233            �           2606    138245    sastoken sastoken_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.sastoken
    ADD CONSTRAINT sastoken_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.sastoken DROP CONSTRAINT sastoken_pkey;
       public            postgres    false    253            |           2606    121189    steps steps_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.steps
    ADD CONSTRAINT steps_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.steps DROP CONSTRAINT steps_pkey;
       public            postgres    false    237            �           2606    135918 ,   user_extracted_data user_extracted_data_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.user_extracted_data
    ADD CONSTRAINT user_extracted_data_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.user_extracted_data DROP CONSTRAINT user_extracted_data_pkey;
       public            postgres    false    247            b           2606    42609    user_info user_info_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.user_info
    ADD CONSTRAINT user_info_pkey PRIMARY KEY (uuid);
 B   ALTER TABLE ONLY public.user_info DROP CONSTRAINT user_info_pkey;
       public            postgres    false    219            p           2606    119655    user_state user_state_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.user_state
    ADD CONSTRAINT user_state_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.user_state DROP CONSTRAINT user_state_pkey;
       public            postgres    false    227            z           2606    121029    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    235            �           2606    42672 /   conversation_state conversation_state_uuid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.conversation_state
    ADD CONSTRAINT conversation_state_uuid_fkey FOREIGN KEY (uuid) REFERENCES public.user_info(uuid);
 Y   ALTER TABLE ONLY public.conversation_state DROP CONSTRAINT conversation_state_uuid_fkey;
       public          postgres    false    219    225    3938            �           2606    42624 +   doc_table_aadhar doc_table_aadhar_uuid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.doc_table_aadhar
    ADD CONSTRAINT doc_table_aadhar_uuid_fkey FOREIGN KEY (uuid) REFERENCES public.user_info(uuid);
 U   ALTER TABLE ONLY public.doc_table_aadhar DROP CONSTRAINT doc_table_aadhar_uuid_fkey;
       public          postgres    false    3938    219    221            �           2606    42648 #   doc_table_dl doc_table_dl_uuid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.doc_table_dl
    ADD CONSTRAINT doc_table_dl_uuid_fkey FOREIGN KEY (uuid) REFERENCES public.user_info(uuid);
 M   ALTER TABLE ONLY public.doc_table_dl DROP CONSTRAINT doc_table_dl_uuid_fkey;
       public          postgres    false    223    219    3938            �           2606    42660 /   doc_table_passport doc_table_passport_uuid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.doc_table_passport
    ADD CONSTRAINT doc_table_passport_uuid_fkey FOREIGN KEY (uuid) REFERENCES public.user_info(uuid);
 Y   ALTER TABLE ONLY public.doc_table_passport DROP CONSTRAINT doc_table_passport_uuid_fkey;
       public          postgres    false    3938    219    224            �           2606    42636 %   doc_table_ssn doc_table_ssn_uuid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.doc_table_ssn
    ADD CONSTRAINT doc_table_ssn_uuid_fkey FOREIGN KEY (uuid) REFERENCES public.user_info(uuid);
 O   ALTER TABLE ONLY public.doc_table_ssn DROP CONSTRAINT doc_table_ssn_uuid_fkey;
       public          postgres    false    219    222    3938            �           2606    120974     messages messages_thread_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_thread_id_fkey FOREIGN KEY (thread_id) REFERENCES public.conversations(thread_id) ON DELETE CASCADE;
 J   ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_thread_id_fkey;
       public          postgres    false    230    3956    231            �           2606    121030    users users_role_id_fkey    FK CONSTRAINT     |   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_role_id_fkey;
       public          postgres    false    235    3960    233           