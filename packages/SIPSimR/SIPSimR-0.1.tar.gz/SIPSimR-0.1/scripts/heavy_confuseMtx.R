#!/usr/bin/Rscript

# init
rm(list=ls())

# opt parsing
suppressPackageStartupMessages(library(docopt))

'usage: heavy_confuseMtx.r [options] <BD_shift> <OTU_table>

options:
  <BD_shift>       BD_shift file.
  <OTU_table>      SIPSim OTU table.
                   ("-" if from STDIN)
  -o=<o>           Basename for output files.
                   [Default: heavy-cMtx]
  --BD=<b>         BD shift cutoff for identifying isotope incorporators.
                   [Default: 0.001]
  --BD_lowH=<hl>   Low-end BD cutoff for determining the "heavy" fractions.
                   [Default: 1.73]
  --BD_highH=<hh>  High-end BD cutoff for determining the "heavy" fractions.
                   [Default: 1.75]		   
  --BD_lowL=<ll>   Low-end BD cutoff for determining the "light" fractions.
                   [Default: 1.68]
  --BD_highL=<hl>  High-end BD cutoff for determining the "light" fractions.
                   [Default: 1.70]		   
  --con=<l>        Libraries that are unlabeled controls. (comma-separated list).
                   [Default: 1]
  --treat=<l>      Libraries that are labeled treatments. (comma-separated list).
                   [Default: 2]
  --method=<m>     heavy-SIP method (see description). [Default: 1]
  -h               Help
description: 
  Use caret to make a confusion matrix comparing
  KNOWN isotope incorporation (based on BD distribution
  shift between pre-incorp and post-incorp BD KDEs) and
  PREDICTED isotope incorporation (all OTUs in "heavy" fractions)
  
  "heavy-SIP" can define incorporators as either:

  1) any taxa IN the "heavy" fractions of the labeled treatment gradients
  2) any taxa IN the "heavy" fractions of the labeled treatment and NOT present in the "heavy" fractions of the control
  3) any taxa IN the "heavy" fractions of the labeled treatment and NOT present in the "light" fractions of the labeled treatment 
  4) any taxa IN the "heavy" fractions of the labeled treatment and NOT present in the "heavy" fractions of the control and NOT present in "light" fractions of the labeled treatment
  
' -> doc

# opt-parse
opts = docopt(doc)
BD_shift.cut = as.numeric(opts[['--BD']])
BD_lowH.cut = as.numeric(opts[['--BD_lowH']])
BD_highH.cut = as.numeric(opts[['--BD_highH']])
BD_lowL.cut = as.numeric(opts[['--BD_lowL']])
BD_highL.cut = as.numeric(opts[['--BD_highL']])
libs_treat = strsplit(opts[['--treat']], split=',')
libs_treat = unlist(libs_treat)
libs_con = strsplit(opts[['--con']], split=',')
libs_con = unlist(libs_con)
hSIP_method = as.character(opts[['--method']])

# packages
pkgs <- c('dplyr', 'tidyr', 'caret')
for(x in pkgs){
  suppressPackageStartupMessages(library(x, character.only=TRUE))
}

#-- main --#
## load OTU table
if(opts[['<OTU_table>']] == '-'){
  con = pipe("cat", "rb")
  df_OTU = read.delim(con, sep='\t')
} else {
  df_OTU = read.delim(opts[['<OTU_table>']], sep='\t')
}
df_shift = read.delim(opts[['BD_shift']], sep='\t')


## calling incorporators
### taxa in 'heavy' fractions of treatment
if(hSIP_method %in% c('1', '2', '3', '4')){
  df_OTU_s = df_OTU %>%
  filter(library %in% libs_treat, BD_min >= BD_lowH.cut, BD_max <= BD_highH.cut) %>%
    group_by(taxon) %>%
      summarize(total_abund = sum(count)) %>%
        ungroup() %>%
          mutate(incorp = ifelse(total_abund > 0, TRUE, FALSE))
} else {
  stop('heavy-SIP method not recognized')
}
### taxa not in 'heavy' fractions of control
if(hSIP_method %in% c('2', '4')){
  #### OTUs in 'heavy' control fractions
  taxa_HC = df_OTU %>%
  filter(library %in% libs_con, BD_min >= BD_lowH.cut, BD_max <= BD_highH.cut) %>%
    group_by(taxon) %>%
      summarize(total_abund = sum(count)) %>%
        ungroup() %>%
          filter(total_abund > 0) %>%
	    .$taxon
  #### calling incorporators
  df_OTU_s = df_OTU_s %>%
    mutate(incorp = ifelse(incorp == TRUE & !(taxon %in% taxa_HC), TRUE, FALSE))
}
### taxa not in 'light' fractions of treatment,
if(hSIP_method %in% c('3','4')){
  #### OTUs in 'light' treatment fractions
  taxa_LT = df_OTU %>%
  filter(library %in% libs_con, BD_min >= BD_lowL.cut, BD_max <= BD_highL.cut) %>%
    group_by(taxon) %>%
      summarize(total_abund = sum(count)) %>%
        ungroup() %>%
          filter(total_abund > 0) %>%
	    .$taxon

  #### calling incorporators
  df_OTU_s = df_OTU_s %>%
    mutate(incorp = ifelse(incorp == TRUE & !(taxon %in% taxa_LT), TRUE, FALSE))
}
#### re-set df_OTU
df_OTU = df_OTU_s
df_OTU_s = NULL

### BD-shift table (reference)
if (ncol(df_shift) == 8){
  df_shift = df_shift %>%
    mutate(incorp = median > BD_shift.cut)
} else {
  df_shift = df_shift %>%
    filter(lib2 == '2') %>%
      dplyr::rename('library' = lib2) %>%
        mutate(incorp = BD_shift > BD_shift.cut)
}
df_shift = df_shift %>%
  filter(library %in% libs_treat)

## making factors of incorporation status
order_incorp = function(x){
  x$incorp = factor(x$incorp, levels=c(TRUE, FALSE))
  return(x)
}
df_shift = order_incorp(df_shift)
df_OTU = order_incorp(df_OTU)

# joining tables
df_shift$taxon = as.character(df_shift$taxon)
df_OTU$taxon = as.character(df_OTU$taxon)
df.j = inner_join(df_shift, df_OTU, c('taxon' = 'taxon'))


# making confusion matrix
## incorp.x = df_shift  (KNOWN)
## incorp.y = qSIP      (PREDICTED)
df.j = df.j %>%
  mutate(incorp.known = incorp.x,
         incorp.pred = incorp.y) %>%
           select(-incorp.x, -incorp.y)

cfs.mtx = function(x){
  mtx = confusionMatrix(x$incorp.pred, x$incorp.known)
  return(mtx)
}

df.j.cmtx = df.j %>%
  group_by(library) %>%
    nest() %>%
      mutate(c.mtx = lapply(data, cfs.mtx)) 


get_tbl = function(obj, key){
  obj[[key]] %>% as.data.frame
}

conv = function(df){
  df = df %>% as.data.frame
  x = rownames(df) %>% as.data.frame
  df = cbind(x, df)
  colnames(df)[1] = 'variables'
  colnames(df)[2] = 'values'
  return(df)
}

df.j.table = df.j.cmtx %>%
  unnest(purrr::map(c.mtx, function(x) x[['table']] %>% as.data.frame)) %>%
    as.data.frame

df.j.overall = df.j.cmtx %>%
  unnest(purrr::map(c.mtx, function(x) x[['overall']] %>% conv)) %>%
    as.data.frame

df.j.byClass = df.j.cmtx %>%
  unnest(purrr::map(c.mtx, function(x) x[['byClass']] %>% conv)) %>%
    as.data.frame


## writing output
### raw data
saveRDS(df.j.cmtx, opts[['-o']])
message('File written: ', opts[['-o']])
outFile = paste(c(opts[['-o']], 'data.txt'), collapse='_')
write.table(df.j, outFile, sep='\t', quote=F, row.names=F)
message('File written: ', outFile)

## confusion matrix data
write_tbl = function(df, outPrefix, outFile){
  outFile = paste(c(outPrefix, outFile), collapse='_')
  write.table(df, file=outFile, sep='\t', quote=FALSE, row.names=FALSE)
  message('File written: ', outFile)
}
write_tbl(df.j.table, opts[['-o']], 'table.txt')
write_tbl(df.j.overall, opts[['-o']], 'overall.txt')
write_tbl(df.j.byClass, opts[['-o']], 'byClass.txt')

