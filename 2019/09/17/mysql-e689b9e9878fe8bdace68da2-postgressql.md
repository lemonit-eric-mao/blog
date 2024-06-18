---
title: 'MySQL 批量转换 PostgresSQL'
date: '2019-09-17T08:10:31+00:00'
status: publish
permalink: /2019/09/17/mysql-%e6%89%b9%e9%87%8f%e8%bd%ac%e6%8d%a2-postgressql
author: 毛巳煜
excerpt: ''
type: post
id: 5041
category:
    - PostgreSQL
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 1.下载转换工具

转换工具： https://github.com/ahammond/mysql2pgsql  
转换工具下载：https://github.com/ahammond/mysql2pgsql.git

##### 1.1 转换工具用法

**`./mysql2pgsql.pl 源sql文件 转换后sql文件`**

##### 2.批量转换

```ruby
[postgres@test1 tools]<span class="katex math inline">pwd
/home/postgres/tools
[postgres@test1 tools]</span>
[postgres@test1 tools]$ cat > convert.sh 
```

##### 2.1 批量转换用法

**`convert.sh 与 mysql2pgsql.pl 在同一目录下`**

```ruby
[postgres@test1 tools]<span class="katex math inline">ll
总用量 60
-rwxrwxrwx 1 postgres postgres   515 9月  17 16:00 convert.sh
drwxrwxrwx 2 tidb     tidb     12288 9月  17 08:45 mysql-20190917
-rwxrwxr-x 1 postgres postgres 42469 9月  17 14:58 mysql2pgsql.pl
[postgres@test1 tools]</span>
[postgres@test1 tools]$ ./convert.sh mysql-20190917/

```

##### 3.批量恢复数据脚本

```ruby
[postgres@test1 tools]$ cat > dump.sh 
```

##### 3.1 批量恢复数据脚本用法

```ruby
[postgres@test1 tools]<span class="katex math inline">ll
总用量 68
-rwxrwxrwx 1 postgres postgres   515 9月  17 16:00 convert.sh
drwxrwxr-x 4 postgres postgres  4096 9月  17 16:11 dist
-rwxrwxr-x 1 postgres postgres   508 9月  17 16:29 dump.sh
drwxrwxrwx 2 tidb     tidb     12288 9月  17 08:45 mysql-20190917
-rwxrwxr-x 1 postgres postgres 42469 9月  17 14:58 mysql2pgsql.pl
[postgres@test1 tools]</span>
[postgres@test1 tools]$ ./dump.sh testdb 172.160.180.47

```

- - - - - -

- - - - - -

- - - - - -

##### mysql2pgsql.pl 源代码

```perl
#!/usr/bin/perl -w
# mysql2pgsql
# MySQL to PostgreSQL dump file converter
#
# For usage: perl mysql2pgsql.perl --help
#
# ddl statments are changed but none or only minimal real data
# formatting are done.
# data consistency is up to the DBA.
#
# Modified by Robert Bruccoleri in 2013 to include skipsets, skipenum, splitinserts, and
# doubleslash options and to remove
# unrecognized options properly for enums, dates, and other fields with constraints.
#
# 2011: changes made by Mischa Spiegelmock for improved BLOB and
# foreign key constraint support
#
# (c) 2004-2007 Jose M Duarte and Joseph Speigle ... gborg
#
# (c) 2000-2004 Maxim Rudensky  <fonin>
# (c) 2000 Valentine Danilchuk  <valdan>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
# This product includes software developed by the Max Rudensky
# and its contributors.
# 4. Neither the name of the author nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

use 5.10.0;         # For ++ Regular expression operator.

use Getopt::Long;

use POSIX;

use strict;
use warnings;


# main sections
# -------------
# 1 variable declarations
# 2 subroutines
# 3 get commandline options and specify help statement
# 4 loop through file and process
# 5. print_plpgsql function prototype

#################################################################
#  1.  variable declarations
#################################################################
# command line options
my( <span class="katex math inline">ENC_IN,</span>ENC_OUT, <span class="katex math inline">PRESERVE_CASE,</span>HELP, <span class="katex math inline">DEBUG,</span>SCHEMA, <span class="katex math inline">LOWERCASE,</span>CHAR2VARCHAR, <span class="katex math inline">NODROP,</span>SEP_FILE,
    <span class="katex math inline">SKIPSETS,</span>SKIPENUM, <span class="katex math inline">SPLITINSERTS,</span>DOUBLESLASH,
    <span class="katex math inline">opt_debug,</span>opt_help, <span class="katex math inline">opt_schema,</span>opt_preserve_case, <span class="katex math inline">opt_char2varchar,</span>opt_nodrop, <span class="katex math inline">opt_sepfile,</span>opt_enc_in, <span class="katex math inline">opt_enc_out );</span>SKIPSETS = 0;
<span class="katex math inline">SKIPENUM = 0;</span>SPLITINSERTS = 0;
<span class="katex math inline">DOUBLESLASH = 1;
# variables for constructing pre-create-table entities
my</span>pre_create_sql='';    # comments, 'enum' constraints preceding create table statement
my <span class="katex math inline">auto_increment_seq= '';    # so we can easily substitute it if we need a default value
my</span>create_sql='';    # all the datatypes in the create table section
my <span class="katex math inline">post_create_sql='';   # create indexes, foreign keys, table comments
my</span>function_create_sql = '';  # for the set (function,trigger) and CURRENT_TIMESTAMP ( function,trigger )
#  constraints
my (<span class="katex math inline">type,</span>column_valuesStr, @column_values, <span class="katex math inline">value );
my %constraints=(); #  holds values constraints used to emulate mysql datatypes (e.g. year, set)
# datatype conversion variables
my (</span>index,<span class="katex math inline">seq);
my (</span>column_name, <span class="katex math inline">col,</span>quoted_column);
my ( @year_holder, <span class="katex math inline">year,</span>constraint_table_name);
my <span class="katex math inline">table="";   # table_name for create sql statements
my</span>table_no_quotes="";   # table_name for create sql statements
my <span class="katex math inline">sl = '^\s+\w+\s+';  # matches the column name
my</span>tables_first_timestamp_column= 1;  #  decision to print warnings about default_timestamp not being in postgres
my <span class="katex math inline">mysql_numeric_datatypes = "TINYINT|SMALLINT|MEDIUMINT|INT|INTEGER|BIGINT|REAL|DOUBLE|FLOAT|DECIMAL|NUMERIC";
my</span>mysql_datetime_datatypes = "|DATE|TIME|TIMESTAMP|DATETIME|YEAR";
my <span class="katex math inline">mysql_text_datatypes = "CHAR|VARCHAR|BINARY|VARBINARY|TINYBLOB|BLOB|MEDIUMBLOB|LONGBLOB|TINYTEXT|TEXT|MEDIUMTEXT|LONGTEXT|ENUM|SET";
my</span>mysql_datatypesStr =  <span class="katex math inline">mysql_numeric_datatypes . "|".</span>mysql_datetime_datatypes . "|". <span class="katex math inline">mysql_text_datatypes ;
# handling INSERT INTO statements
my</span>rowRe = qr{
    \(                  # opening parens
        (               #  (start capture)
            (?:         #  (start group)
            '           # string start
                [^'\\]*     # up to string-end or backslash (escape)
                (?:     #  (start group)
                \\.     # gobble escaped character
                [^'\\]*     # up to string-end of backslash
                )*      #  (end group, repeat zero or more)
            '           # string end
            |           #  (OR)
            .*?         # everything else (not strings)
            )*          #  (end group, repeat zero or more)
        )               #  (end capture)
    \)                  # closing parent
}x;

my (<span class="katex math inline">insert_table,</span>valueString);
#
########################################################
# 2.  subroutines
#
# get_identifier
# print_post_create_sql()
# quote_and_lc()
# make_plpgsql(<span class="katex math inline">table,</span>column_name) -- at end of file
########################################################

# returns an identifier with the given suffix doing controlled
# truncation if necessary
sub get_identifier($$<span class="katex math inline">) {
    my (</span>table, <span class="katex math inline">col,</span>suffix) = @_;
    my <span class="katex math inline">name = '';</span>table=~s/\"//g; # make sure that <span class="katex math inline">table doesn't have quotes so we don't end up with redundant quoting</span>col=~s/\"//g; # do same for column.
    # in the case of multiple columns
    my @cols = split(/,/,<span class="katex math inline">col);</span>col =~ s/,//g;
    # in case all columns together too long we have to truncate them
    if (length(<span class="katex math inline">col) > 55) {
        my</span>totaltocut = length(<span class="katex math inline">col)-55;
        my</span>tocut = ceil(<span class="katex math inline">totaltocut / @cols);
        @cols = map {substr(</span>_,0,abs(length(<span class="katex math inline">_)-</span>tocut))} @cols;
        <span class="katex math inline">col="";
        foreach (@cols){</span>col.=<span class="katex math inline">_;
        }
    }

    my</span>max_table_length = 63 - length("_<span class="katex math inline">{col}_</span>suffix");

    if (length(<span class="katex math inline">table) ></span>max_table_length) {
        <span class="katex math inline">table = substr(</span>table, length(<span class="katex math inline">table) -</span>max_table_length, <span class="katex math inline">max_table_length);
    }
    return quote_and_lc("</span>{table}_<span class="katex math inline">{col}_</span>{suffix}");
}


#
#
# prints comments, indexes, foreign key constraints (the latter 2 possibly to a separate file)
sub print_post_create_sql() {
    my ( @create_idx_comments_constraints_commandsArr, <span class="katex math inline">stmts,</span>table_field_combination);
    my %stmts;
    # loop to check for duplicates in <span class="katex math inline">post_create_sql
    # Needed because of duplicate key declarations ( PRIMARY KEY and KEY), auto_increment columns

    @create_idx_comments_constraints_commandsArr = split(';\n?',</span>post_create_sql);
    if (<span class="katex math inline">SEP_FILE) {
        open(SEP_FILE, ">>:encoding(</span>ENC_OUT)", <span class="katex math inline">SEP_FILE) or die "Unable to open</span>SEP_FILE for output: <span class="katex math inline">!\n";
    }

    foreach (@create_idx_comments_constraints_commandsArr) {
        if (m/CREATE INDEX "*(\S+)"*\s/i) {  #  CREATE INDEX korean_english_wordsize_idx ON korean_english USING btree  (wordsize);</span>table_field_combination =  <span class="katex math inline">1;
            # if this particular table_field_combination was already used do not print the statement:
            if (</span>SEP_FILE) {
                print SEP_FILE "<span class="katex math inline">_;\n" if !defined(</span>stmts{<span class="katex math inline">table_field_combination});
            } else {
                print OUT "</span>_;\n" if !defined(<span class="katex math inline">stmts{</span>table_field_combination});
            }
            <span class="katex math inline">stmts{</span>table_field_combination} = 1;
        }
        elsif (m/COMMENT/i) {  # COMMENT ON object IS 'text'; but comment may be part of table name so use 'elsif'
            print OUT "<span class="katex math inline">_;\n"
        } else {  # foreign key constraint  or comments (those preceded by -- )
            if (</span>SEP_FILE) {
                print SEP_FILE "<span class="katex math inline">_;\n";
            } else {
                print OUT "</span>_;\n"
            }
        }
    }

    if (<span class="katex math inline">SEP_FILE) {
        close SEP_FILE;
    }</span>post_create_sql='';
    # empty %constraints for next " create table" statement
}

# quotes a string or a multicolumn string (comma separated)
# and optionally lowercase (if LOWERCASE is set)
# lowercase .... if user wants default postgres behavior
# quotes .... to preserve keywords and to preserve case when case-sensitive tables are to be used
sub quote_and_lc(<span class="katex math inline">)
{
    my</span>col = shift;
    if (<span class="katex math inline">LOWERCASE) {</span>col = lc(<span class="katex math inline">col);
    }
    if (</span>col =~ m/,/) {
        my @cols = split(/,\s?/, <span class="katex math inline">col);
        @cols = map {"\"</span>_\""} @cols;
        return join(', ', @cols);
    } else {
        return "\"<span class="katex math inline">col\"";
    }
}

########################################################
# 3.  get commandline options and maybe print help
########################################################

GetOptions("help",
       "debug"=> \$opt_debug,
       "schema=s" => \$SCHEMA,
       "preserve_case" => \$opt_preserve_case,
       "char2varchar" => \$opt_char2varchar,
       "nodrop" => \$opt_nodrop,
       "sepfile=s" => \$opt_sepfile,
       "enc_in=s" => \$opt_enc_in,
       "enc_out=s" => \$opt_enc_out,
       "skipsets!" => \$SKIPSETS,
       "skipenum!" => \$SKIPENUM,
       "splitinserts!" => \$SPLITINSERTS,
       "doubleslash!" => \$DOUBLESLASH);</span>HELP = <span class="katex math inline">opt_help || 0;</span>DEBUG = <span class="katex math inline">opt_debug || 0;</span>PRESERVE_CASE = <span class="katex math inline">opt_preserve_case || 0;
if (</span>PRESERVE_CASE == 1) { <span class="katex math inline">LOWERCASE = 0; }
else {</span>LOWERCASE = 1; }
<span class="katex math inline">CHAR2VARCHAR =</span>opt_char2varchar || 0;
<span class="katex math inline">NODROP =</span>opt_nodrop || 0;
<span class="katex math inline">SEP_FILE =</span>opt_sepfile || 0;
<span class="katex math inline">ENC_IN =</span>opt_enc_in || 'utf8';
<span class="katex math inline">ENC_OUT =</span>opt_enc_out || 'utf8';

if ((<span class="katex math inline">HELP) || ! defined(</span>ARGV[0]) || ! defined(<span class="katex math inline">ARGV[1])) {
    print "\n\nUsage: perl</span>0 {--help --debug --preserve_case --char2varchar --nodrop --schema --sepfile --enc_in --enc_out } mysql.sql pg.sql\n";
    print "\t* OPTIONS WITHOUT ARGS\n";
    print "\t--help:  prints this message \n";
    print "\t--debug: output the commented-out mysql line above the postgres line in pg.sql \n";
    print "\t--preserve_case: prevents automatic case-lowering of column and table names\n";
    print "\t\tIf you want to preserve case, you must set this flag. For example,\n";
    print "\t\tIf your client application quotes table and column-names and they have cases in them, set this flag\n";
    print "\t--char2varchar: converts all char fields to varchar\n";
    print "\t--nodrop: strips out DROP TABLE statements\n";
    print "\t--[no]skipsets: skip generating constraints for sets\n";
    print "\t--[no]skipenum: skip generating constraints for enum\n";
    print "\t--[no]splitinserts: split multi-record inserts into separate insert commands.\n";
    print "\t--[no]doubleslash: to control the doubling of backslashes in escaped strings.\n";
    print "\t\totherise harmless warnings are printed by psql when the dropped table does not exist\n";
    print "\n\t* OPTIONS WITH ARGS\n";
    print "\t--schema: outputs a line into the postgres sql file setting search_path \n";
    print "\t--sepfile: output foreign key constraints and indexes to a separate file so that it can be\n";
    print "\t\timported after large data set is inserted from another dump file\n";
    print "\t--enc_in: encoding of mysql in file (default utf8) \n";
    print "\t--enc_out: encoding of postgres out file (default utf8) \n";
    print "\n\t* REQUIRED ARGUMENTS\n";
    if (defined (<span class="katex math inline">ARGV[0])) {
        print "\tmysql.sql (</span>ARGV[0])\n";
    } else {
        print "\tmysql.sql (undefined)\n";
    }
    if (defined (<span class="katex math inline">ARGV[1])) {
        print "\tpg.sql (</span>ARGV[1])\n";
    } else {
        print "\tpg.sql (undefined)\n";
    }
    print "\n";
    exit 1;
}
########################################################
# 4.  process through mysql_dump.sql file
# in a big loop
########################################################

# open in and out files
open(IN,"<:encoding die="" dump="" file="" mysql="" open="">:encoding(<span class="katex math inline">ENC_OUT)",</span>ARGV[1]) || die "can't open pg dump file <span class="katex math inline">ARGV[1]";

# output header
print OUT "--\n";
print OUT "-- Generated from mysql2pgsql.perl\n";
print OUT "-- http://gborg.postgresql.org/project/mysql2psql/\n";
print OUT "-- (c) 2001 - 2007 Jose M. Duarte, Joseph Speigle\n";
print OUT "--\n";
print OUT "\n";
print OUT "-- warnings are printed for drop tables if they do not exist\n";
print OUT "-- please see http://archives.postgresql.org/pgsql-novice/2004-10/msg00158.php\n\n";
print OUT "-- ##############################################################\n";

if (</span>SCHEMA ) {
    print OUT "set search_path='" . $SCHEMA . "'\\g\n" ;
}

# loop through mysql file  on a per-line basis
while(<in>) {

##############     flow     #########################
# (the lines are directed to different string variables at different times)
#
# handle drop table , unlock, connect statements
# if ( start of create table)   {
#   print out post_create table (indexes, foreign key constraints, comments from previous table)
#   add drop table statement if !<span class="katex math inline">NODROP to pre_create_sql
#   next;
# }
# else if ( inside create table) {
#   add comments in this portion to create_sql
#   if ( end of create table) {
#      delete mysql-unique CREATE TABLE commands
#      print pre_create_sql
#      print the constraint tables for set and year datatypes
#      print create_sql
#      print function_create_sql (this is for the enum columns only)
#      next;
#   }
#   do substitutions
#    -- NUMERIC DATATYPES
#    -- CHARACTER DATATYPES
#    -- DATE AND TIME DATATYPES
#    -- KEY AND UNIQUE CREATIONS
#    and append them to create_sql
# } else {
#   print inserts on-the-spot (this script only changes default timestamp of 0000-00-00)
# }
# LOOP until EOF
#
########################################################


if (!/^\s*insert into/i) { # not inside create table so don't worry about data corruption
    s/`//g;  #  '`pgsql uses no backticks to denote table name (CREATE TABLE `sd`) or around field
            # and table names like  mysql
            # doh!  we hope all dashes and special chars are caught by the regular expressions :)
}
if (/^\s*USE\s*([^;]*);/) {
    print OUT "\\c ".</span>1;
    next;
}
if (/^(UN)?LOCK TABLES/i  || /drop\s+table/i ) {

    # skip
    # DROP TABLE is added when we see the CREATE TABLE
    next;
}
if (/^SET \@saved_cs_client/ || /^SET character_set_client = \@saved_cs_client/ || /^SET character_set_client = utf8/) {
    # skip non-sql mysql bullshit
    next;
}
if (/(create\s+table\s+)([-_\w]+)\s/i) { #  example: CREATE TABLE `english_english`
    <span class="katex math inline">tables_first_timestamp_column= 1;  #  decision to print warnings about default_timestamp not being in postgres</span>create_sql = '';
    <span class="katex math inline">table_no_quotes =</span>2 ;
    print "Dumping <span class="katex math inline">table_no_quotes...\n";</span>table=quote_and_lc(<span class="katex math inline">2);
    if ( !</span>NODROP )  {  # always print drop table if user doesn't explicitly say not to
        #  to drop a table that is referenced by a view or a foreign-key constraint of another table,
        #  CASCADE must be specified. (CASCADE will remove a dependent view entirely, but in the
        #  in the foreign-key case it will only remove the foreign-key constraint, not the other table entirely.)
        #  (source: 8.1.3 docs, section "drop table")
        warn "table <span class="katex math inline">table will be dropped CASCADE\n";</span>pre_create_sql .= "DROP TABLE <span class="katex math inline">table CASCADE\\g\n";    # custom dumps may be missing the 'dump' commands
    }

    s/(create\s+table\s+)([-_\w]+)\s/</span>1 <span class="katex math inline">table /i;
    if (</span>DEBUG) {
        <span class="katex math inline">create_sql .=  '-- ' .</span>_;
    }
    <span class="katex math inline">create_sql .=</span>_;
    next;
}
if (<span class="katex math inline">create_sql ne "") {         # we are inside create table statement so lets process datatypes
    # print out comments or empty lines in context
    if (</span>DEBUG) {
        <span class="katex math inline">create_sql .=  '-- ' .</span>_;
    }
    if (/^#/ || /^<span class="katex math inline">/ || /^\s*--/) {
        s/^#/--/;   #  Two hyphens (--) is the SQL-92 standard indicator for comments</span>create_sql.=$_;
        next;
    }

    if (/\).*;/i) {    # end of create table squence

        s/INSERT METHOD[=\s+][^;\s]+//i;
        s/PASSWORD=[^;\s]+//i;
        s/ROW_FORMAT=(?:DEFAULT|DYNAMIC|FIXED|COMPRESSED|REDUNDANT|COMPACT)+//i;
        s/DELAY KEY WRITE=[^;\s]+//i;
        s/INDEX DIRECTORY[=\s+][^;\s]+//i;
        s/DATA DIRECTORY=[^;\s]+//i;
        s/CONNECTION=[^;\s]+//i;
        s/CHECKSUM=[^;\s]+//i;
        s/Type=[^;\s]+//i; # ISAM ,   # older versions
        s/COLLATE=[^;\s]+//i;         # table's collate
        s/COLLATE\s+[^;\s]+//i;         # table's collate
        # possible AUTO_INCREMENT starting index, it is used in mysql 5.0.26, not sure since which version
        if (/AUTO_INCREMENT=(\d+)/i) {
        # should take   CREATE SEQUENCE "rhm_host_info_id_seq" START WITH 16;
        my <span class="katex math inline">start_value =</span>1;
        #print <span class="katex math inline">auto_increment_seq . " seq --\n";
        # print</span>pre_create_sql . "--\n";
        <span class="katex math inline">pre_create_sql =~ s/(CREATE SEQUENCE</span>auto_increment_seq )/<span class="katex math inline">1 START WITH</span>start_value /;
    }
        s/AUTO_INCREMENT=\d+//i;
        s/PACK_KEYS=\d//i;            # mysql 5.0.22
        s/DEFAULT CHARSET=[^;\s]+//i; #  my mysql version is 4.1.11
        s/ENGINE\s*=\s*[^;\s]+//i;   #  my mysql version is 4.1.11
        s/ROW_FORMAT=[^;\s]+//i;   #  my mysql version is 5.0.22
        s/MIN_ROWS=[^;\s]+//i;
        s/MAX_ROWS=[^;\s]+//i;
        s/AVG_ROW_LENGTH=[^;\s]+//i;
        if (/COMMENT='([^']*)'/) {  # ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='must be country zones';
            <span class="katex math inline">post_create_sql.="COMMENT ON TABLE</span>table IS '<span class="katex math inline">1'\;"; # COMMENT ON table_name IS 'text';
            s/COMMENT='[^']*'//i;
        }</span>create_sql =~ s/,<span class="katex math inline">//g;    # strip last , inside create table
        # make sure we end in a comma, as KEY statments are turned
        # into post_create_sql indices
        # they often are the last line so leaving a 'hanging comma'
        my @array = split("\n",</span>create_sql);
        for (my <span class="katex math inline">a =</span>#array; <span class="katex math inline">a >= 0;</span>a--) {  #loop backwards
            if (<span class="katex math inline">a ==</span>#array  && <span class="katex math inline">array[</span>a] =~ m/,\s*<span class="katex math inline">/) {    # for last line</span>array[<span class="katex math inline">a] =~ s/,\s*</span>//;
                next;
            }
            if (<span class="katex math inline">array[</span>a] !~ m/create table/i) {  # i.e. if there was more than one column in table
                if (<span class="katex math inline">a !=</span>#array  && <span class="katex math inline">array[</span>a] !~ m/,\s*<span class="katex math inline">/  ) {  # for second to last</span>array[<span class="katex math inline">a] =~ s/</span>/,/;
                    last;
                }
                elsif (<span class="katex math inline">a !=</span>#array  && <span class="katex math inline">array[</span>a] =~ m/,\s*<span class="katex math inline">/ ) {  # for second to last
                    last;
                }
            }
        }</span>create_sql = join("\n", @array) . "\n";
        <span class="katex math inline">create_sql .=</span>_;

        # put comments out first
        print OUT <span class="katex math inline">pre_create_sql;

        # create separate table to reference and to hold mysql's possible set data-type
        # values.  do that table's creation before create table
        # definition
        foreach</span>column_name (keys %constraints) {
            <span class="katex math inline">type=</span>constraints{<span class="katex math inline">column_name}{'type'};</span>column_valuesStr = <span class="katex math inline">constraints{</span>column_name}{'values'};
            <span class="katex math inline">constraint_table_name = get_identifier(</span>{table},<span class="katex math inline">{column_name} ,"constraint_table");
            if (lc(</span>type) eq 'set') {
                print OUT qq~DROP TABLE <span class="katex math inline">constraint_table_name  CASCADE\\g\n~ ;
                print OUT qq~create table</span>constraint_table_name  ( set_values varchar UNIQUE)\\g\n~ ;
                <span class="katex math inline">function_create_sql .= make_plpgsql(</span>table,<span class="katex math inline">column_name);
            } elsif (lc(</span>type) eq 'year')  {
                print OUT qq~DROP TABLE <span class="katex math inline">constraint_table_name  CASCADE\\g\n~ ;
                print OUT qq~create table</span>constraint_table_name  ( year_values varchar UNIQUE)\\g\n~ ;
            }
            @column_values = split /,/, <span class="katex math inline">column_valuesStr;  #/
            foreach</span>value (@column_values) {
                print OUT qq~insert into <span class="katex math inline">constraint_table_name   values (</span>value  )\\g\n~; # ad ' for ints and varchars
            }
        }

        # print create table and reset create table vars
        # when moving from each "create table" to "insert" part of dump
        print OUT <span class="katex math inline">create_sql;
        print OUT</span>function_create_sql;
        <span class="katex math inline">pre_create_sql="";</span>auto_increment_seq="";
        <span class="katex math inline">create_sql="";</span>function_create_sql='';
        %constraints=();
        # the post_create_sql for this table is output at the beginning of the next table def
        # in case we want to make indexes after doing inserting
        next;
    }
    if (/^\s*(\w+)\s+.*COMMENT\s*'([^']*)'/) {  #`zone_country_id` int(11) COMMENT 'column comment here',
        <span class="katex math inline">quoted_column=quote_and_lc(</span>1);
        <span class="katex math inline">post_create_sql.="COMMENT ON COLUMN</span>table"."."." <span class="katex math inline">quoted_column IS '</span>2'\;"; # COMMENT ON table_name.column_name IS 'text';
        s/COMMENT\s*'[^']*'//i;
    }


    # NUMERIC DATATYPES
    #
    # auto_increment -> sequences
    # UNSIGNED conversions
    # TINYINT
    # SMALLINT
    # MEDIUMINT
    # INT, INTEGER
    # BIGINT
    #
    # DOUBLE [PRECISION], REAL
    # DECIMAL(M,D), NUMERIC(M,D)
    # FLOAT(p)
    # FLOAT

    s/(\w*int)\(\d+\)/<span class="katex math inline">1/g;  # hack of the (n) stuff for e.g. mediumint(2) int(3)

    if (/^(\s*)(\w+)\s*.*numeric.*auto_increment/i) {         # int,auto_increment -> serial</span>seq = get_identifier(<span class="katex math inline">table,</span>2, 'seq');
        <span class="katex math inline">quoted_column=quote_and_lc(</span>2);
        # Smash datatype to int8 and autogenerate the sequence.
        s/^(\s*)(\w+)\s*.*NUMERIC(.*)auto_increment([^,]*)/<span class="katex math inline">1</span>quoted_column serial8 <span class="katex math inline">4/ig;</span>create_sql.=<span class="katex math inline">_;
        next;
    }
    if (/^\s*(\w+)\s+.*int.*auto_increment/i) {  #  example: data_id mediumint(8) unsigned NOT NULL auto_increment,</span>seq = get_identifier(<span class="katex math inline">table,</span>1, 'seq');
        <span class="katex math inline">quoted_column=quote_and_lc(</span>1);
        s/(\s*)(\w+)\s+.*int.*auto_increment([^,]*)/<span class="katex math inline">1</span>quoted_column serial8 <span class="katex math inline">3/ig;</span>create_sql.=<span class="katex math inline">_;
        next;
    }




    # convert UNSIGNED to CHECK constraints
    if (m/^(\s*)(\w+)\s+((float|double|double precision|real|decimal|numeric))(.*)unsigned/i) {</span>quoted_column = quote_and_lc(<span class="katex math inline">2);
        s/^(\s*)(\w+)\s+((float|double|double precision|real|decimal|numeric))(.*)unsigned/</span>1 <span class="katex math inline">quoted_column</span>3 <span class="katex math inline">4 CHECK (</span>quoted_column >= 0)/i;
    }
    # example:  `wordsize` tinyint(3) unsigned default NULL,
    if (m/^(\s+)(\w+)\s+(\w+)\s+unsigned/i) {
        <span class="katex math inline">quoted_column=quote_and_lc(</span>2);
        s/^(\s+)(\w+)\s+(\w+)\s+unsigned/<span class="katex math inline">1</span>quoted_column <span class="katex math inline">3 CHECK (</span>quoted_column >= 0)/i;
    }
    if (m/^(\s*)(\w+)\s+(bigint.*)unsigned/) {
        <span class="katex math inline">quoted_column=quote_and_lc(</span>2);
        #  see http://archives.postgresql.org/pgsql-general/2005-07/msg01178.php
        #  and see http://www.postgresql.org/docs/8.2/interactive/datatype-numeric.html
        # see  http://dev.mysql.com/doc/refman/5.1/en/numeric-types.html  max size == 20 digits
        s/^(\s*)(\w+)\s+bigint(.*)unsigned/<span class="katex math inline">1</span>quoted_column NUMERIC (20,0) CHECK (<span class="katex math inline">quoted_column >= 0)/i;

    }

    # int type conversion
    # TINYINT    (signed) -128 to 127 (unsigned) 0   255
    #  SMALLINT A small integer. The signed range is -32768 to 32767. The unsigned range is 0 to 65535.
    #  MEDIUMINT  A medium-sized integer. The signed range is -8388608 to 8388607. The unsigned range is 0 to 16777215.
    #  INT A normal-size integer. The signed range is -2147483648 to 2147483647. The unsigned range is 0 to 4294967295.
    # BIGINT The signed range is -9223372036854775808 to 9223372036854775807. The unsigned range is 0 to 18446744073709551615
    # for postgres see http://www.postgresql.org/docs/8.2/static/datatype-numeric.html#DATATYPE-INT
    s/^(\s+"*\w+"*\s+)tinyint/</span>1 smallint/i;
    s/^(\s+"*\w+"*\s+)mediumint/<span class="katex math inline">1 integer/i;

    # the floating point types
    #   double -> double precision
    #   double(n,m) -> double precision
    #   float - no need for conversion
    #   float(n) - no need for conversion
    #   float(n,m) -> double precision

    s/(^\s*\w+\s+)double(\(\d+,\d+\))?/</span>1double precision/i;
    s/float(\(\d+,\d+\))/double precision/i;

    #
    # CHARACTER TYPES
    #
    # set
    # enum
    # binary(M), VARBINARy(M), tinyblob, tinytext,
    # bit
    # char(M), varchar(M)
    # blob -> text
    # mediumblob
    # longblob, longtext
    # text -> text
    # mediumtext
    # longtext
    #  mysql docs: A BLOB is a binary large object that can hold a variable amount of data.

    # Change location because the enum test can leave a collation around.

    # nuke column's collate and character set
    s/(\S+)\s+character\s+set\s+\w+/<span class="katex math inline">1/gi;
    s/(\S+)\s+collate\s+\w+/</span>1/gi;
    # Likewise to zerofill.
    s/(\S+)\s+zerofill\s+\w+/<span class="katex math inline">1/gi;

    # set
    # For example, a column specified as SET('one', 'two') NOT NULL can have any of these values:
    # ''
    # 'one'
    # 'two'
    # 'one,two'
    if (/(\w*)\s+set\(((?:['"]\w+['"]\s*,*)+(?:['"]\w+['"])*)\)(.*)</span>/i) { # example:  `au_auth` set('r','w','d') NOT NULL default '',
        <span class="katex math inline">column_name =</span>1;
        unless (<span class="katex math inline">SKIPSETS) {</span>constraints{<span class="katex math inline">column_name}{'values'} =</span>2;  # 'abc','def', ...
        <span class="katex math inline">constraints{</span>column_name}{'type'} = "set";  # 'abc','def', ...
    }
        <span class="katex math inline">_ =  qq~</span>column_name varchar , \n~;
        <span class="katex math inline">column_name = quote_and_lc(</span>1);
        <span class="katex math inline">create_sql.=</span>_;
        next;

    }
    if (/(\S*)\s+enum\(((?:['"][^'"]+['"]\s*,)+['"][^'"]+['"])\)(.*)<span class="katex math inline">/i) { # enum handling
        #  example:  `test` enum('?','+','-') NOT NULL default '?'
        #</span>2  is the values of the enum 'abc','def', ...
        <span class="katex math inline">quoted_column=quote_and_lc(</span>1);
        #  "test" NOT NULL default '?' CONSTRAINT test_test_constraint CHECK ("test" IN ('?','+','-'))
        if (<span class="katex math inline">SKIPENUM) {</span>_ = qq~ <span class="katex math inline">quoted_column text, \n~;
        }
        else {</span>_ = qq~ <span class="katex math inline">quoted_column varchar CHECK (</span>quoted_column IN ( <span class="katex math inline">2 ))</span>3\n~;  # just assume varchar?
    }
        <span class="katex math inline">create_sql.=</span>_;
        next;
    }
    # Take care of "binary" option for char and varchar
    # (pre-4.1.2, it indicated a byte array; from 4.1.2, indicates
    # a binary collation)
    s/(?:var)?char(?:\(\d+\))? (?:byte|binary)/bytea/i;
    if (m/(?:var)?binary\s*\(\d+\)/i) {   #  c varBINARY(3) in Mysql
        warn "WARNING in table '<span class="katex math inline">table' '</span>_':  binary type is converted to bytea (unsized) for Postgres\n";
    }
    s/(?:var)?binary(?:\(\d+\))?/bytea/i;   #  c varBINARY(3) in Mysql
    s/bit(?:\(\d+\))?/bytea/i;   #  bit datatype -> bytea

    # large datatypes
    s/\w*blob/bytea/gi;
    s/tinytext/text/gi;
    s/mediumtext/text/gi;
    s/longtext/text/gi;

    # char -> varchar -- if specified as a command line option
    # PostgreSQL would otherwise pad with spaces as opposed
    # to MySQL! Your user interface may depend on this!
    if (<span class="katex math inline">CHAR2VARCHAR) {
        s/(^\s+\S+\s+)char/</span>{1}varchar/gi;
    }


    #
    # DATE AND TIME TYPES
    #
    # date  time
    # year
    # datetime
    # timestamp

    # date  time
    # these are the same types in postgres, just do the replacement of 0000-00-00 date

    if (m/default '(\d+)-(\d+)-(\d+)([^']*)'/i) { # we grab the year, month and day
        # NOTE: times of 00:00:00 are possible and are okay
        my <span class="katex math inline">time = '';
        my</span>year=<span class="katex math inline">1;
        my</span>month= <span class="katex math inline">2;
        my</span>day = <span class="katex math inline">3;
        if (</span>4) {
            <span class="katex math inline">time =</span>4;
        }
        if (<span class="katex math inline">year eq "0000") {</span>year = '1970'; }
        if (<span class="katex math inline">month eq "00") {</span>month = '01'; }
        if (<span class="katex math inline">day eq "00") {</span>day = '01'; }
        s/default '[^']+'/default '<span class="katex math inline">year-</span>month-<span class="katex math inline">day</span>time'/i; # finally we replace with <span class="katex math inline">datetime
    }

    # convert mysql's year datatype to a constraint
    if (/(\w*)\s+year\(4\)(.*)</span>/i) { # can be integer OR string 1901-2155
        <span class="katex math inline">constraint_table_name = get_identifier(</span>table,<span class="katex math inline">1 ,"constraint_table");</span>column_name=quote_and_lc(<span class="katex math inline">1);
        @year_holder = ();</span>year='';
        for (1901 .. 2155) {
        <span class="katex math inline">year = "'</span>_'";
        unless (<span class="katex math inline">year =~ /2155/) {</span>year .= ','; }
        push( @year_holder, <span class="katex math inline">year);
        }</span>constraints{<span class="katex math inline">column_name}{'values'} = join('','',@year_holder);   # '1901','1902', ...</span>constraints{<span class="katex math inline">column_name}{'type'} = "year";
    my</span>constraint_name = &get_identifier(<span class="katex math inline">table,</span>column_name, "constraint");
    <span class="katex math inline">_ =  qq~</span>column_name varchar CONSTRAINT <span class="katex math inline">{constraint_name} REFERENCES</span>constraint_table_name ("year_values") <span class="katex math inline">2\n~;</span>create_sql.=<span class="katex math inline">_;
        next;
    } elsif (/(\w*)\s+year\(2\)(.*)</span>/i) { # same for a 2-integer string
        <span class="katex math inline">constraint_table_name = get_identifier(</span>table,<span class="katex math inline">1 ,"constraint_table");</span>column_name=quote_and_lc(<span class="katex math inline">1);
        @year_holder = ();</span>year='';
        for (1970 .. 2069) {
            <span class="katex math inline">year = "'</span>_'";
            if (<span class="katex math inline">year =~ /2069/) { next; }
            push( @year_holder,</span>year);
        }
        push( @year_holder, '0000');
        <span class="katex math inline">constraints{</span>column_name}{'values'} = join(',',@year_holder);   # '1971','1972', ...
        <span class="katex math inline">constraints{</span>column_name}{'type'} = "year";  # 'abc','def', ...
    my <span class="katex math inline">constraint_name = &get_identifier(</span>table, <span class="katex math inline">column_name, "constraint");</span>_ =  qq~ <span class="katex math inline">1 varchar CONSTRAINT</span>{constraint_name} REFERENCES <span class="katex math inline">constraint_table_name ("year_values")</span>2\n~;
        <span class="katex math inline">create_sql.=</span>_;
        next;
    }

    # datetime
    # Default on a dump from MySQL 5.0.22 is in the same form as datetime so let it flow down
    # to the timestamp section and deal with it there
    s/(<span class="katex math inline">{sl})datetime /</span>1timestamp without time zone /i;

    # change not null datetime field to null valid ones
    # (to support remapping of "zero time" to null
    # s/(<span class="katex math inline">sl)datetime not null/</span>1timestamp without time zone/i;


    # timestamps
    #
    # nuke datetime representation (not supported in PostgreSQL)
    # change default time of 0000-00-00 to 1970-01-01

    # we may possibly need to create a trigger to provide
    # equal functionality with ON UPDATE CURRENT TIMESTAMP


    if (m/<span class="katex math inline">{sl}timestamp/i) {
        if ( m/ON UPDATE CURRENT_TIMESTAMP/i )  {  # the ... default CURRENT_TIMESTAMP  only applies for blank inserts, not updates
            s/ON UPDATE CURRENT_TIMESTAMP//i ;
            m/^\s*(\w+)\s+timestamp/i ;
            # automatic trigger creation</span>table_no_quotes =~ s/"//g;
<span class="katex math inline">function_create_sql .= " CREATE OR REPLACE FUNCTION update_".</span>table_no_quotes . "() RETURNS trigger AS '
BEGIN
    NEW.<span class="katex math inline">1 := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
' LANGUAGE 'plpgsql';

-- before INSERT is handled by 'default CURRENT_TIMESTAMP'
CREATE TRIGGER add_current_date_to_".</span>table_no_quotes." BEFORE UPDATE ON ". <span class="katex math inline">table . " FOR EACH ROW EXECUTE PROCEDURE
update_".</span>table_no_quotes."();\n";

        }
        if (<span class="katex math inline">tables_first_timestamp_column && m/DEFAULT NULL/i) {
            # DEFAULT NULL is the same as DEFAULT CURRENT_TIMESTAMP for the first TIMESTAMP  column. (MYSQL manual)
            s/(</span>sl)(timestamp\s+)default null/<span class="katex math inline">1</span>2 DEFAULT CURRENT_TIMESTAMP/i;
        }
        <span class="katex math inline">tables_first_timestamp_column= 0;
        if (m/</span>{sl}timestamp\s*\(\d+\)/i) {   # fix for timestamps with width spec not handled (ID: 1628)
            warn "WARNING for in table '<span class="katex math inline">table' '</span>_': your default timestamp width is being ignored for table <span class="katex math inline">table \n";
            s/(</span>sl)timestamp(?:\(\d+\))/<span class="katex math inline">1datetime/i;
        }
    } # end timestamp section

    # KEY AND UNIQUE CREATIONS
    #
    # unique
    if ( /^\s+unique\s+\(([^(]+)\)/i ) { #  example    UNIQUE `name` (`name`), same as UNIQUE KEY
        #  POSTGRESQL:  treat same as mysql unique</span>quoted_column = quote_and_lc(<span class="katex math inline">1);
        s/\s+unique\s+\(([^(]+)\)/ unique (</span>quoted_column) /i;
            <span class="katex math inline">create_sql.=</span>_;
        next;
        } elsif ( /^\s+unique\s+key\s*(\w+)\s*\(([^(]+)\)/i ) { #  example    UNIQUE KEY `name` (`name`)
            #  MYSQL: unique  key: allows null=YES, allows duplicates=NO (*)
            #  ... new ... UNIQUE KEY `unique_fullname` (`fullname`)  in my mysql v. Ver 14.12 Distrib 5.1.7-beta
            #  POSTGRESQL:  treat same as mysql unique
        # just quote columns
        <span class="katex math inline">quoted_column = quote_and_lc(</span>2);
            s/\s+unique\s+key\s*(\w+)\s*\(([^(]+)\)/ unique (<span class="katex math inline">quoted_column) /i;</span>create_sql.=<span class="katex math inline">_;
        # the index corresponding to the 'key' is automatically created
            next;
    }
    # keys
    if ( /^\s+fulltext key\s+/i) { # example:  FULLTEXT KEY `commenttext` (`commenttext`)
    # that is key as a word in the first check for a match
        # the tsvector datatype is made for these types of things
        # example mysql file:
        #  what is tsvector datatype?
        #  http://www.sai.msu.su/~megera/postgres/gist/tsearch/V2/docs/tsearch-V2-intro.html
        warn "dba must do fulltext key transformation for</span>table\n";
        next;
    }
    if ( /^(\s+)constraint (\S+) foreign key \(([^)]+)\) references (\S+) \(([^)]+)\)(.*)/i ) {
        <span class="katex math inline">quoted_column =quote_and_lc(</span>3);
        <span class="katex math inline">col=quote_and_lc(</span>5);
        <span class="katex math inline">post_create_sql .= "ALTER TABLE</span>table ADD FOREIGN KEY (<span class="katex math inline">quoted_column) REFERENCES " . quote_and_lc(</span>4) . " (<span class="katex math inline">col);\n";
        next;
    }
    if ( /^\s*primary key\s*\(([^)]+)\)([,\s]+)/i ) { #  example    PRIMARY KEY (`name`)
        # MYSQL: primary key: allows null=NO , allows duplicates=NO
        #  POSTGRESQL: When an index is declared unique, multiple table rows with equal indexed values will not be
        #       allowed. Null values are not considered equal.
        #  POSTGRESQL quote's source: 8.1.3 docs section 11.5 "unique indexes"
        #  so, in postgres, we need to add a NOT NULL to the UNIQUE constraint
        # and, primary key (mysql) == primary key (postgres) so that we *really* don't need change anything</span>quoted_column = quote_and_lc(<span class="katex math inline">1);
        s/(\s*)primary key\s+\(([^)]+)\)([,\s]+)/</span>1 primary key (<span class="katex math inline">quoted_column)</span>3/i;
        # indexes are automatically created for unique columns
        <span class="katex math inline">create_sql.=</span>_;
        next;
    } elsif (m/^\s+key\s[-_\s\w]+\((.+)\)/i    ) {     # example:   KEY `idx_mod_english_def_word` (`word`),
        # regular key: allows null=YES, allows duplicates=YES
        # MYSQL:   KEY is normally a synonym for INDEX.  http://dev.mysql.com/doc/refman/5.1/en/create-table.html
        #
        #  * MySQL: ALTER TABLE {<span class="katex math inline">table} ADD KEY</span>column (<span class="katex math inline">column)
        #  * PostgreSQL: CREATE INDEX {</span>table}_<span class="katex math inline">column_idx ON {</span>table}(<span class="katex math inline">column) // Please note the _idx "extension"
        #    PRIMARY KEY (`postid`),
        #    KEY `ownerid` (`ownerid`)
        # create an index for everything which has a key listed for it.
        my</span>col = <span class="katex math inline">1;
        # TODO we don't have a translation for the substring syntax in text columns in MySQL (e.g. "KEY my_idx (mytextcol(20))")
        # for now just getting rid of the brackets and numbers (the substring specifier):</span>col=~s/\(\d+\)//g;
        <span class="katex math inline">quoted_column = quote_and_lc(</span>col);
        if (<span class="katex math inline">col =~ m/,/) {</span>col =  s/,/_/;
        }
        <span class="katex math inline">index = get_identifier(</span>table, <span class="katex math inline">col, 'idx');</span>post_create_sql.="CREATE INDEX <span class="katex math inline">index ON</span>table USING btree (<span class="katex math inline">quoted_column)\;";
        # just create index do not add to create table statement
        next;
    }

    # handle 'key' declared at end of column
    if (/\w+.*primary key/i) {   # mysql: key is normally just a synonym for index
    # just leave as is ( postgres has primary key type)


    } elsif (/(\w+\s+(?:</span>mysql_datatypesStr)\s+.*)key/i) {   # mysql: key is normally just a synonym for index
    # I can't find a reference for 'key' in a postgres command without using the word 'primary key'
        s/<span class="katex math inline">1key/</span>1/i ;
        <span class="katex math inline">index = get_identifier(</span>table, <span class="katex math inline">1, 'idx');</span>quoted_column =quote_and_lc(<span class="katex math inline">1);</span>post_create_sql.="CREATE INDEX <span class="katex math inline">index ON</span>table USING btree (<span class="katex math inline">quoted_column) \;";</span>create_sql.=<span class="katex math inline">_;
    }



    # do we really need this anymore?
    # remap colums with names of existing system attribute
    if (/"oid"/i) {
        s/"oid"/"_oid"/g;
        print STDERR "WARNING: table</span>table uses column \"oid\" which is renamed to \"_oid\"\nYou should fix application manually! Press return to continue.";
        my $wait=<stdin>;
    }

    s/oid/_oid/i if (/key/i && /oid/i); # fix oid in key

    # FINAL QUOTING OF ALL COLUMNS
    # quote column names which were not already quoted
    # perhaps they were not quoted because they were not explicitly handled
    if (!/^\s*"(\w+)"(\s+)/i) {
        /^(\s*)(\w+)(\s+)(.*)<span class="katex math inline">/i ;</span>quoted_column= quote_and_lc(<span class="katex math inline">2);
        s/^(\s*)(\w+)(\s+)(.*)</span>/<span class="katex math inline">1</span>quoted_column <span class="katex math inline">3</span>4 /;
    }
    <span class="katex math inline">create_sql.=</span>_;
    #  END of if (<span class="katex math inline">create_sql ne "") i.e. were inside create table statement so processed datatypes
}
# add "not in create table" comments or empty lines to pre_create_sql
elsif (/^#/ || /^</span>/ || /^\s*--/) {
    s/^#/--/;   #  Two hyphens (--) is the SQL-92 standard indicator for comments
    <span class="katex math inline">pre_create_sql .=</span>_ ;  # printed above create table statement
    next;
}
elsif (/^\s*insert into/i) { # not inside create table and doing insert
    # fix mysql's zero/null value for timestamps
    s/'0000-00-00/'1970-01-01/gi;
    # commented out to fix bug "Field contents interpreted as a timestamp", what was the point of this line anyway?
    #s/([12]\d\d\d)([01]\d)([0-3]\d)([0-2]\d)([0-6]\d)([0-6]\d)/'<span class="katex math inline">1-</span>2-<span class="katex math inline">3</span>4:<span class="katex math inline">5:</span>6'/;

    #---- fix data in inserted data: (from MS world)
    s!\x96!-!g;    # --
    s!\x93!"!g;    # ``
    s!\x94!"!g;    # ''
    s!\x85!... !g;    # \ldots
    s!\x92!`!g;

    print OUT <span class="katex math inline">pre_create_sql;    # print comments preceding the insert section</span>pre_create_sql="";
    <span class="katex math inline">auto_increment_seq = "";

    s/'((?:[^'\\]++|\\.)*+)'(?=[),])/E'</span>1'/g;
    # for the E'' see http://www.postgresql.org/docs/8.2/interactive/release-8-1.html
    if (<span class="katex math inline">DOUBLESLASH) {
    s!\\\\!\\\\\\\\!g;      # replace \\ with ]\\\\
    }

    # convert escaped hex BLOB data
    s/([,\(])0x([0-9A-F]+)([,\)])/</span>1E'\\\\x<span class="katex math inline">2'</span>3/g;

    # split 'extended' INSERT INTO statements to something PostgreSQL can  understand
    ( <span class="katex math inline">insert_table,</span>valueString) = <span class="katex math inline">_ =~ m/^INSERT\s+INTO\s+['`"]*(.*?)['`"]*\s+VALUES\s*(.*)/i;</span>insert_table = quote_and_lc(<span class="katex math inline">insert_table);
    s/^INSERT INTO.*?\);//i;  # hose the statement which is to be replaced whether a run-on or not
    if (</span>SPLITINSERTS) {
    my @rows = <span class="katex math inline">valueString =~ m/</span>rowRe/g;

    if (@rows > 1) {
        for my <span class="katex math inline">row (@rows) {
        print OUT qq(INSERT INTO</span>insert_table VALUES (<span class="katex math inline">row);\n);
        }
        # end command
        print OUT  "\n";
    }
    else {
        print OUT qq(INSERT INTO</span>insert_table VALUES <span class="katex math inline">valueString \n);
    }
    }
    else {   # guarantee table names are quoted
        print OUT qq(INSERT INTO</span>insert_table VALUES <span class="katex math inline">valueString \n);
    }
} else {
    print OUT</span>_ ;  #  example: /*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
}
#  keep looping and get next line of IN file

} # END while(<in>)

print_post_create_sql();   # in case there is extra from the last table

#################################################################
#  5.  print_plgsql function prototype
#      emulate the set datatype with the following plpgsql function
#      looks ugly so putting at end of file
#################################################################
#
sub make_plpgsql {
my (<span class="katex math inline">table,</span>column_name) = (<span class="katex math inline">_[0],</span>_[1]);
<span class="katex math inline">table=~s/\"//g; # make sure that</span>table doesn't have quotes so we don't end up with redundant quoting
my <span class="katex math inline">constraint_table = get_identifier(</span>table,<span class="katex math inline">column_name ,"constraint_table");
return "
-- this function is called by the insert/update trigger
-- it checks if the INSERT/UPDATE for the 'set' column
-- contains members which comprise a valid mysql set
-- this TRIGGER function therefore acts like a constraint
--  provided limited functionality for mysql's set datatype
-- just verifies and matches for string representations of the set at this point
-- though the set datatype uses bit comparisons, the only supported arguments to our
-- set datatype are VARCHAR arguments
-- to add a member to the set add it to the ".</span>table."_".<span class="katex math inline">column_name." table
CREATE OR REPLACE FUNCTION check_".</span>table."_".<span class="katex math inline">column_name."_set(  ) RETURNS TRIGGER AS \$\$\n
DECLARE
----
arg_str VARCHAR ;
argx VARCHAR := '';
nobreak INT := 1;
rec_count INT := 0;
psn INT := 0;
str_in VARCHAR := NEW.</span>column_name;
----
BEGIN
----
IF str_in IS NULL THEN RETURN NEW ; END IF;
arg_str := REGEXP_REPLACE(str_in, '\\',\\'', ',');  -- str_in is CONSTANT
arg_str := REGEXP_REPLACE(arg_str, '^\\'', '');
arg_str := REGEXP_REPLACE(arg_str, '\\'\<span class="katex math inline">', '');
-- RAISE NOTICE 'arg_str %',arg_str;
psn := POSITION(',' in arg_str);
IF psn > 0 THEN
    psn := psn - 1; -- minus-1 from comma position
    -- RAISE NOTICE 'psn %',psn;
    argx := SUBSTRING(arg_str FROM 1 FOR psn);  -- get one set member
    psn := psn + 2; -- go to first starting letter
    arg_str := SUBSTRING(arg_str FROM psn);   -- hack it off
ELSE
    psn := 0; -- minus-1 from comma position
    argx := arg_str;
END IF;
-- RAISE NOTICE 'argx %',argx;
-- RAISE NOTICE 'new arg_str: %',arg_str;
WHILE nobreak LOOP
    EXECUTE 'SELECT count(*) FROM</span>constraint_table WHERE set_values = ' || quote_literal(argx) INTO rec_count;
    IF rec_count = 0 THEN RAISE EXCEPTION 'one of the set values was not found';
    END IF;
    IF psn > 0 THEN
        psn := psn - 1; -- minus-1 from comma position
        -- RAISE NOTICE 'psn %',psn;
        argx := SUBSTRING(arg_str FROM 1 FOR psn);  -- get one set member
        psn := psn + 2; -- go to first starting letter
        arg_str := SUBSTRING(arg_str FROM psn);   -- hack it off
        psn := POSITION(',' in arg_str);
    ELSE nobreak = 0;
    END IF;
    -- RAISE NOTICE 'next argx % and next arg_str %', argx, arg_str;
END LOOP;
RETURN NEW;
----
END;
\<span class="katex math inline">\$ LANGUAGE 'plpgsql' VOLATILE;

drop trigger set_test ON</span>table;
-- make a trigger for each set field
-- make trigger and hard-code in column names
-- see http://archives.postgresql.org/pgsql-interfaces/2005-02/msg00020.php
CREATE   TRIGGER    set_test
BEFORE   INSERT OR   UPDATE  ON <span class="katex math inline">table   FOR  EACH  ROW
EXECUTE  PROCEDURE  check_".</span>table."_".$column_name."_set();\n";
} #  end sub make_plpgsql();

</in></stdin></in></:encoding></valdan></fonin>
```