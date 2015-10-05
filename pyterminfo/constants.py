from . utils import *

__all__ = [
    'BOOLEAN_CAPABILITIES'
  , 'CAPABILITY_ARITY'
  , 'CAPABILITY_VARNAMES'
  , 'NUMERIC_CAPABILITIES'
  , 'STRING_CAPABILITIES'
  , 'TERMINFO_MAGIC'
  , 'VARIABLE_SLOTS'
  ]


##################################################
#                                                #
##################################################
TERMINFO_MAGIC = 0x11A

##################################################
#                                                #
##################################################
BOOLEAN_CAPABILITIES = [
    'bw'       , 'am'      , 'xsb'   , 'xhp'   , 'xenl'   , 'eo'      , 'gn'     , 'hc'
  , 'km'       , 'hs'      , 'in'    , 'da'    , 'db'     , 'mir'     , 'msgr'   , 'os'
  , 'eslok'    , 'xt'      , 'hz'    , 'ul'    , 'xon'    , 'nxon'    , 'mc5i'   , 'chts'
  , 'nrrmc'    , 'npc'     , 'ndscr' , 'ccc'   , 'bce'    , 'hls'     , 'xhpa'   , 'crxm'
  , 'daisy'    , 'xvpa'    , 'sam'   , 'cpix'  , 'lpix'
  ]

NUMERIC_CAPABILITIES = [
    'cols'     , 'it'      , 'lines' , 'lm'    , 'xmc'    , 'pb'      , 'vt'     , 'wsl'
  , 'nlab'     , 'lh'      , 'lw'    , 'ma'    , 'wnum'   , 'colors'  , 'pairs'  , 'ncv'
  , 'bufsz'    , 'spinv'   , 'spinh' , 'maddr' , 'mjump'  , 'mcs'     , 'mls'    , 'npins'
  , 'orc'      , 'orl'     , 'orhi'  , 'orvi'  , 'cps'    , 'widcs'   , 'btns'   , 'bitwin'
  , 'bitype'
  ]

STRING_CAPABILITIES = [
    'cbt'      , 'bel'     , 'cr'    , 'csr'   , 'tbc'    , 'clear'   , 'el'     , 'ed'
  , 'hpa'      , 'cmdch'   , 'cup'   , 'cud1'  , 'home'   , 'civis'   , 'cub1'   , 'mrcup'
  , 'cnorm'    , 'cuf1'    , 'll'    , 'cuu1'  , 'cvvis'  , 'dch1'    , 'dl1'    , 'dsl'
  , 'hd'       , 'smacs'   , 'blink' , 'bold'  , 'smcup'  , 'smdc'    , 'dim'    , 'smir'
  , 'invis'    , 'prot'    , 'rev'   , 'smso'  , 'smul'   , 'ech'     , 'rmacs'  , 'sgr0'
  , 'rmcup'    , 'rmdc'    , 'rmir'  , 'rmso'  , 'rmul'   , 'flash'   , 'ff'     , 'fsl'
  , 'is1'      , 'is2'     , 'is3'   , 'if'    , 'ich1'   , 'il1'     , 'ip'     , 'kbs'
  , 'ktbc'     , 'kclr'    , 'kctab' , 'kdch1' , 'kdl1'   , 'kcud1'   , 'krmir'  , 'kel'
  , 'ked'      , 'kf0'     , 'kf1'   , 'kf10'  , 'kf2'    , 'kf3'     , 'kf4'    , 'kf5'
  , 'kf6'      , 'kf7'     , 'kf8'   , 'kf9'   , 'khome'  , 'kich1'   , 'kil1'   , 'kcub1'
  , 'kll'      , 'knp'     , 'kpp'   , 'kcuf1' , 'kind'   , 'kri'     , 'khts'   , 'kcuu1'
  , 'rmkx'     , 'smkx'    , 'lf0'   , 'lf1'   , 'lf10'   , 'lf2'     , 'lf3'    , 'lf4'
  , 'lf5'      , 'lf6'     , 'lf7'   , 'lf8'   , 'lf9'    , 'rmm'     , 'smm'    , 'nel'
  , 'pad'      , 'dch'     , 'dl'    , 'cud'   , 'ich'    , 'indn'    , 'il'     , 'cub'
  , 'cuf'      , 'rin'     , 'cuu'   , 'pfkey' , 'pfloc'  , 'pfx'     , 'mc0'    , 'mc4'
  , 'mc5'      , 'rep'     , 'rs1'   , 'rs2'   , 'rs3'    , 'rf'      , 'rc'     , 'vpa'
  , 'sc'       , 'ind'     , 'ri'    , 'sgr'   , 'hts'    , 'wind'    , 'ht'     , 'tsl'
  , 'uc'       , 'hu'      , 'iprog' , 'ka1'   , 'ka3'    , 'kb2'     , 'kc1'    , 'kc3'
  , 'mc5p'     , 'rmp'     , 'acsc'  , 'pln'   , 'kcbt'   , 'smxon'   , 'rmxon'  , 'smam'
  , 'rmam'     , 'xonc'    , 'xoffc' , 'enacs' , 'smln'   , 'rmln'    , 'kbeg'   , 'kcan'
  , 'kclo'     , 'kcmd'    , 'kcpy'  , 'kcrt'  , 'kend'   , 'kent'    , 'kext'   , 'kfnd'
  , 'khlp'     , 'kmrk'    , 'kmsg'  , 'kmov'  , 'knxt'   , 'kopn'    , 'kopt'   , 'kprv'
  , 'kprt'     , 'krdo'    , 'kref'  , 'krfr'  , 'krpl'   , 'krst'    , 'kres'   , 'ksav'
  , 'kspd'     , 'kund'    , 'kBEG'  , 'kCAN'  , 'kCMD'   , 'kCPY'    , 'kCRT'   , 'kDC'
  , 'kDL'      , 'kslt'    , 'kEND'  , 'kEOL'  , 'kEXT'   , 'kFND'    , 'kHLP'   , 'kHOM'
  , 'kIC'      , 'kLFT'    , 'kMSG'  , 'kMOV'  , 'kNXT'   , 'kOPT'    , 'kPRV'   , 'kPRT'
  , 'kRDO'     , 'kRPL'    , 'kRIT'  , 'kRES'  , 'kSAV'   , 'kSPD'    , 'kUND'   , 'rfi'
  , 'kf11'     , 'kf12'    , 'kf13'  , 'kf14'  , 'kf15'   , 'kf16'    , 'kf17'   , 'kf18'
  , 'kf19'     , 'kf20'    , 'kf21'  , 'kf22'  , 'kf23'   , 'kf24'    , 'kf25'   , 'kf26'
  , 'kf27'     , 'kf28'    , 'kf29'  , 'kf30'  , 'kf31'   , 'kf32'    , 'kf33'   , 'kf34'
  , 'kf35'     , 'kf36'    , 'kf37'  , 'kf38'  , 'kf39'   , 'kf40'    , 'kf41'   , 'kf42'
  , 'kf43'     , 'kf44'    , 'kf45'  , 'kf46'  , 'kf47'   , 'kf48'    , 'kf49'   , 'kf50'
  , 'kf51'     , 'kf52'    , 'kf53'  , 'kf54'  , 'kf55'   , 'kf56'    , 'kf57'   , 'kf58'
  , 'kf59'     , 'kf60'    , 'kf61'  , 'kf62'  , 'kf63'   , 'el1'     , 'mgc'    , 'smgl'
  , 'smgr'     , 'fln'     , 'sclk'  , 'dclk'  , 'rmclk'  , 'cwin'    , 'wingo'  , 'hup'
  , 'dial'     , 'qdial'   , 'tone'  , 'pulse' , 'hook'   , 'pause'   , 'wait'   , 'u0'
  , 'u1'       , 'u2'      , 'u3'    , 'u4'    , 'u5'     , 'u6'      , 'u7'     , 'u8'
  , 'u9'       , 'op'      , 'oc'    , 'initc' , 'initp'  , 'scp'     , 'setf'   , 'setb'
  , 'cpi'      , 'lpi'     , 'chr'   , 'cvr'   , 'defc'   , 'swidm'   , 'sdrfq'  , 'sitm'
  , 'slm'      , 'smicm'   , 'snlq'  , 'snrmq' , 'sshm'   , 'ssubm'   , 'ssupm'  , 'sum'
  , 'rwidm'    , 'ritm'    , 'rlm'   , 'rmicm' , 'rshm'   , 'rsubm'   , 'rsupm'  , 'rum'
  , 'mhpa'     , 'mcud1'   , 'mcub1' , 'mcuf1' , 'mvpa'   , 'mcuu1'   , 'porder' , 'mcud'
  , 'mcub'     , 'mcuf'    , 'mcuu'  , 'scs'   , 'smgb'   , 'smgbp'   , 'smglp'  , 'smgrp'
  , 'smgt'     , 'smgtp'   , 'sbim'  , 'scsd'  , 'rbim'   , 'rcsd'    , 'subcs'  , 'supcs'
  , 'docr'     , 'zerom'   , 'csnm'  , 'kmous' , 'minfo'  , 'reqmp'   , 'getm'   , 'setaf'
  , 'setab'    , 'pfxl'    , 'devt'  , 'csin'  , 's0ds'   , 's1ds'    , 's2ds'   , 's3ds'
  , 'smglr'    , 'smgtb'   , 'birep' , 'binel' , 'bicr'   , 'colornm' , 'defbi'  , 'endbi'
  , 'setcolor' , 'slines'  , 'dispc' , 'smpch' , 'rmpch'  , 'smsc'    , 'rmsc'   , 'pctrm'
  , 'scesc'    , 'scesa'   , 'ehhlm' , 'elhlm' , 'elohlm' , 'erhlm'   , 'ethlm'  , 'evhlm'
  , 'sgr1'     , 'slength'
  ]

CAPABILITY_ARITY = {
    'csr'      : 2             , 'hpa'     : 1              , 'cup'     : 2
  , 'mrcup'    : 2             , 'ech'     : 1              , 'dch'     : 1
  , 'dl'       : 1             , 'cud'     : 1              , 'ich'     : 1
  , 'indn'     : 1             , 'il'      : 1              , 'cub'     : 1
  , 'cuf'      : 1             , 'rin'     : 1              , 'cuu'     : 1
  , 'pfkey'    : 2             , 'pfloc'   : 2              , 'pfx'     : 2
  , 'rep'      : 2             , 'vpa'     : 1              , 'sgr'     : 9
  , 'wind'     : 4             , 'tsl'     : 1              , 'mc5p'    : 1
  , 'pln'      : 2             , 'sclk'    : 3              , 'cwin'    : 5
  , 'wingo'    : 1             , 'dial'    : 1              , 'qdial'   : 1
  , 'initc'    : 4             , 'initp'   : 7              , 'scp'     : 1
  , 'setf'     : 1             , 'setb'    : 1              , 'cpi'     : 1
  , 'lpi'      : 1             , 'chr'     : 1              , 'cvr'     : 1
  , 'defc'     : 3             , 'mvpa'    : 1              , 'scs'     : 1
  , 'smgbp'    : 2             , 'smglp'   : 1              , 'smgrp'   : 1
  , 'smgtp'    : 1             , 'scsd'    : 2              , 'rcsd'    : 1
  , 'csnm'     : 1             , 'getm'    : 1              , 'setaf'   : 1
  , 'setab'    : 1             , 'pfxl'    : 3              , 'smglr'   : 2
  , 'smgtb'    : 2             , 'birep'   : 2              , 'colornm' : 1
  , 'setcolor' : 1             , 'slines'  : 1              , 'dispc'   : 1
  , 'sgr1'     : None          , 'slength' : 1
  }

CAPABILITY_VARNAMES = {
    'acsc'     : 'acs_chars'                , 'am'       : 'auto_right_margin'         , 'bce'      : 'back_color_erase'
  , 'bel'      : 'bell'                     , 'bicr'     : 'bit_image_carriage_return' , 'binel'    : 'bit_image_newline'
  , 'birep'    : 'bit_image_repeat'         , 'bitwin'   : 'bit_image_entwining'       , 'bitype'   : 'bit_image_type'
  , 'blink'    : 'enter_blink_mode'         , 'bold'     : 'enter_bold_mode'           , 'btns'     : 'buttons'
  , 'bufsz'    : 'buffer_capacity'          , 'bw'       : 'auto_left_margin'          , 'cbt'      : 'back_tab'
  , 'ccc'      : 'can_change'               , 'chr'      : 'change_res_horz'           , 'chts'     : 'hard_cursor'
  , 'civis'    : 'cursor_invisible'         , 'clear'    : 'clear_screen'              , 'cmdch'    : 'command_character'
  , 'cnorm'    : 'cursor_normal'            , 'colornm'  : 'color_names'               , 'colors'   : 'max_colors'
  , 'cols'     : 'columns'                  , 'cpi'      : 'change_char_pitch'         , 'cpix'     : 'cpi_changes_res'
  , 'cps'      : 'print_rate'               , 'cr'       : 'carriage_return'           , 'crxm'     : 'cr_cancels_micro_mode'
  , 'csin'     : 'code_set_init'            , 'csnm'     : 'char_set_names'            , 'csr'      : 'change_scroll_region'
  , 'cub'      : 'parm_left_cursor'         , 'cub1'     : 'cursor_left'               , 'cud'      : 'parm_down_cursor'
  , 'cud1'     : 'cursor_down'              , 'cuf'      : 'parm_right_cursor'         , 'cuf1'     : 'cursor_right'
  , 'cup'      : 'cursor_address'           , 'cuu'      : 'parm_up_cursor'            , 'cuu1'     : 'cursor_up'
  , 'cvr'      : 'change_res_vert'          , 'cvvis'    : 'cursor_visible'            , 'cwin'     : 'create_window'
  , 'da'       : 'memory_above'             , 'daisy'    : 'has_print_wheel'           , 'db'       : 'memory_below'
  , 'dch'      : 'parm_dch'                 , 'dch1'     : 'delete_character'          , 'dclk'     : 'display_clock'
  , 'defbi'    : 'define_bit_image_region'  , 'defc'     : 'define_char'               , 'devt'     : 'device_type'
  , 'dial'     : 'dial_phone'               , 'dim'      : 'enter_dim_mode'            , 'dispc'    : 'display_pc_char'
  , 'dl'       : 'parm_delete_line'         , 'dl1'      : 'delete_line'               , 'docr'     : 'these_cause_cr'
  , 'dsl'      : 'dis_status_line'          , 'ech'      : 'erase_chars'               , 'ed'       : 'clr_eos'
  , 'ehhlm'    : 'enter_horizontal_hl_mode' , 'el'       : 'clr_eol'                   , 'el1'      : 'clr_bol'
  , 'elhlm'    : 'enter_left_hl_mode'       , 'elohlm'   : 'enter_low_hl_mode'         , 'enacs'    : 'ena_acs'
  , 'endbi'    : 'end_bit_image_region'     , 'eo'       : 'erase_overstrike'          , 'erhlm'    : 'enter_right_hl_mode'
  , 'eslok'    : 'status_line_esc_ok'       , 'ethlm'    : 'enter_top_hl_mode'         , 'evhlm'    : 'enter_vertical_hl_mode'
  , 'ff'       : 'form_feed'                , 'flash'    : 'flash_screen'              , 'fln'      : 'label_format'
  , 'fsl'      : 'from_status_line'         , 'getm'     : 'get_mouse'                 , 'gn'       : 'generic_type'
  , 'hc'       : 'hard_copy'                , 'hd'       : 'down_half_line'            , 'hls'      : 'hue_lightness_saturation'
  , 'home'     : 'cursor_home'              , 'hook'     : 'flash_hook'                , 'hpa'      : 'column_address'
  , 'hs'       : 'has_status_line'          , 'ht'       : 'tab'                       , 'hts'      : 'set_tab'
  , 'hu'       : 'up_half_line'             , 'hup'      : 'hangup'                    , 'hz'       : 'tilde_glitch'
  , 'ich'      : 'parm_ich'                 , 'ich1'     : 'insert_character'          , 'if'       : 'init_file'
  , 'il'       : 'parm_insert_line'         , 'il1'      : 'insert_line'               , 'in'       : 'insert_null_glitch'
  , 'ind'      : 'scroll_forward'           , 'indn'     : 'parm_index'                , 'initc'    : 'initialize_color'
  , 'initp'    : 'initialize_pair'          , 'invis'    : 'enter_secure_mode'         , 'ip'       : 'insert_padding'
  , 'iprog'    : 'init_prog'                , 'is1'      : 'init_1string'              , 'is2'      : 'init_2string'
  , 'is3'      : 'init_3string'             , 'it'       : 'init_tabs'                 , 'kBEG'     : 'key_sbeg'
  , 'kBEG3'    : 'key_abeg'                 , 'kBEG5'    : 'key_cbeg'                  , 'kBS'      : 'key_sbackspace'
  , 'kBS3'     : 'key_abackspace'           , 'kBS5'     : 'key_cbackspace'            , 'kCAN'     : 'key_scancel'
  , 'kCAN3'    : 'key_acancel'              , 'kCAN5'    : 'key_ccancel'               , 'kCMD'     : 'key_scommand'
  , 'kCMD3'    : 'key_acommand'             , 'kCMD5'    : 'key_ccommand'              , 'kCPY'     : 'key_scopy'
  , 'kCPY3'    : 'key_acopy'                , 'kCPY5'    : 'key_ccopy'                 , 'kCRT'     : 'key_screate'
  , 'kCRT3'    : 'key_acreate'              , 'kCRT5'    : 'key_ccreate'               , 'kDC'      : 'key_sdc'
  , 'kDC3'     : 'key_adc'                  , 'kDC5'     : 'key_cdc'                   , 'kDL'      : 'key_sdl'
  , 'kDL3'     : 'key_adl'                  , 'kDL5'     : 'key_cdl'                   , 'kDOWN'    : 'key_sdown'
  , 'kDOWN3'   : 'key_adown'                , 'kDOWN5'   : 'key_cdown'                 , 'kEND'     : 'key_send'
  , 'kEND3'    : 'key_aend'                 , 'kEND5'    : 'key_cend'                  , 'kEOL'     : 'key_seol'
  , 'kEOL3'    : 'key_aeol'                 , 'kEOL5'    : 'key_ceol'                  , 'kEXT'     : 'key_sexit'
  , 'kEXT3'    : 'key_aexit'                , 'kEXT5'    : 'key_cexit'                 , 'kFND'     : 'key_sfind'
  , 'kFND3'    : 'key_afind'                , 'kFND5'    : 'key_cfind'                 , 'kHLP'     : 'key_shelp'
  , 'kHLP3'    : 'key_ahelp'                , 'kHLP5'    : 'key_chelp'                 , 'kHOM'     : 'key_shome'
  , 'kHOM3'    : 'key_ahome'                , 'kHOM5'    : 'key_chome'                 , 'kIC'      : 'key_sic'
  , 'kIC3'     : 'key_aic'                  , 'kIC5'     : 'key_cic'                   , 'kLFT'     : 'key_sleft'
  , 'kLFT3'    : 'key_aleft'                , 'kLFT5'    : 'key_cleft'                 , 'kMOV'     : 'key_smove'
  , 'kMOV3'    : 'key_amove'                , 'kMOV5'    : 'key_cmove'                 , 'kMSG'     : 'key_smessage'
  , 'kMSG3'    : 'key_amessage'             , 'kMSG5'    : 'key_cmessage'              , 'kNXT'     : 'key_snext'
  , 'kNXT3'    : 'key_anext'                , 'kNXT5'    : 'key_cnext'                 , 'kOPT'     : 'key_soptions'
  , 'kOPT3'    : 'key_aoptions'             , 'kOPT5'    : 'key_coptions'              , 'kPRT'     : 'key_sprint'
  , 'kPRT3'    : 'key_aprint'               , 'kPRT5'    : 'key_cprint'                , 'kPRV'     : 'key_sprevious'
  , 'kPRV3'    : 'key_aprevious'            , 'kPRV5'    : 'key_cprevious'             , 'kRDO'     : 'key_sredo'
  , 'kRDO3'    : 'key_aredo'                , 'kRDO5'    : 'key_credo'                 , 'kRES'     : 'key_srsume'
  , 'kRES3'    : 'key_arsume'               , 'kRES5'    : 'key_crsume'                , 'kRIT'     : 'key_sright'
  , 'kRIT3'    : 'key_aright'               , 'kRIT5'    : 'key_cright'                , 'kRPL'     : 'key_sreplace'
  , 'kRPL3'    : 'key_areplace'             , 'kRPL5'    : 'key_creplace'              , 'kSAV'     : 'key_ssave'
  , 'kSAV3'    : 'key_asave'                , 'kSAV5'    : 'key_csave'                 , 'kSPD'     : 'key_ssuspend'
  , 'kSPD3'    : 'key_asuspend'             , 'kSPD5'    : 'key_csuspend'              , 'kUND'     : 'key_sundo'
  , 'kUND3'    : 'key_aundo'                , 'kUND5'    : 'key_cundo'                 , 'kUP'      : 'key_sup'
  , 'kUP3'     : 'key_aup'                  , 'kUP5'     : 'key_cup'                   , 'kb2'      : 'key_b2'
  , 'kbeg'     : 'key_beg'                  , 'kbs'      : 'key_backspace'             , 'kc1'      : 'key_c1'
  , 'kc3'      : 'key_c3'                   , 'kcub1'    : 'key_left'                  , 'kcud1'    : 'key_down'
  , 'kcuf1'    : 'key_right'                , 'kcup'     : 'key_c_up'                  , 'kcuu1'    : 'key_up'
  , 'kdch1'    : 'key_dc'                   , 'kdl1'     : 'key_dl'                    , 'ked'      : 'key_eos'
  , 'kel'      : 'key_eol'                  , 'kend'     : 'key_end'                   , 'kent'     : 'key_enter'
  , 'kext'     : 'key_exit'                 , 'kf0'      : 'key_f0'                    , 'kf1'      : 'key_f1'
  , 'kf10'     : 'key_f10'                  , 'kf11'     : 'key_f11'                   , 'kf12'     : 'key_f12'
  , 'kf13'     : 'key_f13'                  , 'kf14'     : 'key_f14'                   , 'kf15'     : 'key_f15'
  , 'kf16'     : 'key_f16'                  , 'kf17'     : 'key_f17'                   , 'kf18'     : 'key_f18'
  , 'kf19'     : 'key_f19'                  , 'kf2'      : 'key_f2'                    , 'kf20'     : 'key_f20'
  , 'kf21'     : 'key_f21'                  , 'kf22'     : 'key_f22'                   , 'kf23'     : 'key_f23'
  , 'kf24'     : 'key_f24'                  , 'kf25'     : 'key_f25'                   , 'kf26'     : 'key_f26'
  , 'kf27'     : 'key_f27'                  , 'kf28'     : 'key_f28'                   , 'kf29'     : 'key_f29'
  , 'kf3'      : 'key_f3'                   , 'kf30'     : 'key_f30'                   , 'kf31'     : 'key_f31'
  , 'kf32'     : 'key_f32'                  , 'kf33'     : 'key_f33'                   , 'kf34'     : 'key_f34'
  , 'kf35'     : 'key_f35'                  , 'kf36'     : 'key_f36'                   , 'kf37'     : 'key_f37'
  , 'kf38'     : 'key_f38'                  , 'kf39'     : 'key_f39'                   , 'kf4'      : 'key_f4'
  , 'kf40'     : 'key_f40'                  , 'kf41'     : 'key_f41'                   , 'kf42'     : 'key_f42'
  , 'kf43'     : 'key_f43'                  , 'kf44'     : 'key_f44'                   , 'kf45'     : 'key_f45'
  , 'kf46'     : 'key_f46'                  , 'kf47'     : 'key_f47'                   , 'kf48'     : 'key_f48'
  , 'kf49'     : 'key_f49'                  , 'kf5'      : 'key_f5'                    , 'kf50'     : 'key_f50'
  , 'kf51'     : 'key_f51'                  , 'kf52'     : 'key_f52'                   , 'kf53'     : 'key_f53'
  , 'kf54'     : 'key_f54'                  , 'kf55'     : 'key_f55'                   , 'kf56'     : 'key_f56'
  , 'kf57'     : 'key_f57'                  , 'kf58'     : 'key_f58'                   , 'kf59'     : 'key_f59'
  , 'kf6'      : 'key_f6'                   , 'kf60'     : 'key_f60'                   , 'kf61'     : 'key_f61'
  , 'kf62'     : 'key_f62'                  , 'kf63'     : 'key_f63'                   , 'kf7'      : 'key_f7'
  , 'kf8'      : 'key_f8'                   , 'kf9'      : 'key_f9'                    , 'kfnd'     : 'key_find'
  , 'khlp'     : 'key_help'                 , 'khome'    : 'key_home'                  , 'khts'     : 'key_stab'
  , 'kich1'    : 'key_ic'                   , 'kil1'     : 'key_il'                    , 'kind'     : 'key_sf'
  , 'kll'      : 'key_ll'                   , 'km'       : 'has_meta_key'              , 'kmous'    : 'key_mouse'
  , 'kmov'     : 'key_move'                 , 'kmrk'     : 'key_mark'                  , 'kmsg'     : 'key_message'
  , 'knp'      : 'key_npage'                , 'knxt'     : 'key_next'                  , 'kopn'     : 'key_open'
  , 'kopt'     : 'key_options'              , 'kpp'      : 'key_ppage'                 , 'kprt'     : 'key_print'
  , 'kprv'     : 'key_previous'             , 'krdo'     : 'key_redo'                  , 'kref'     : 'key_reference'
  , 'kres'     : 'key_resume'               , 'krfr'     : 'key_refresh'               , 'kri'      : 'key_sr'
  , 'krmir'    : 'key_eic'                  , 'krpl'     : 'key_replace'               , 'krst'     : 'key_restart'
  , 'ksav'     : 'key_save'                 , 'kslt'     : 'key_select'                , 'kspd'     : 'key_suspend'
  , 'ktbc'     : 'key_catab'                , 'kund'     : 'key_undo'                  , 'lf0'      : 'lab_f0'
  , 'lf1'      : 'lab_f1'                   , 'lf10'     : 'lab_f10'                   , 'lf2'      : 'lab_f2'
  , 'lf3'      : 'lab_f3'                   , 'lf4'      : 'lab_f4'                    , 'lf5'      : 'lab_f5'
  , 'lf6'      : 'lab_f6'                   , 'lf7'      : 'lab_f7'                    , 'lf8'      : 'lab_f8'
  , 'lf9'      : 'lab_f9'                   , 'lh'       : 'label_height'              , 'lines'    : 'lines'
  , 'll'       : 'cursor_to_ll'             , 'lm'       : 'lines_of_memory'           , 'lpi'      : 'change_line_pitch'
  , 'lpix'     : 'lpi_changes_res'          , 'lw'       : 'label_width'               , 'ma'       : 'max_attributes'
  , 'maddr'    : 'max_micro_address'        , 'mc0'      : 'print_screen'              , 'mc4'      : 'prtr_off'
  , 'mc5'      : 'prtr_on'                  , 'mc5i'     : 'prtr_silent'               , 'mc5p'     : 'prtr_non'
  , 'mcs'      : 'micro_col_size'           , 'mcub'     : 'parm_left_micro'           , 'mcub1'    : 'micro_left'
  , 'mcud'     : 'parm_down_micro'          , 'mcud1'    : 'micro_down'                , 'mcuf'     : 'parm_right_micro'
  , 'mcuf1'    : 'micro_right'              , 'mcuu'     : 'parm_up_micro'             , 'mcuu1'    : 'micro_up'
  , 'mgc'      : 'clear_margins'            , 'mhpa'     : 'micro_column_address'      , 'minfo'    : 'mouse_info'
  , 'mir'      : 'move_insert_mode'         , 'mjump'    : 'max_micro_jump'            , 'mls'      : 'micro_line_size'
  , 'mrcup'    : 'cursor_mem_address'       , 'msgr'     : 'move_standout_mode'        , 'mvpa'     : 'micro_row_address'
  , 'ncv'      : 'no_color_video'           , 'ndscr'    : 'non_dest_scroll_region'    , 'nel'      : 'newline'
  , 'nlab'     : 'num_labels'               , 'npc'      : 'no_pad_char'               , 'npins'    : 'number_of_pins'
  , 'nrrmc'    : 'non_rev_rmcup'            , 'nxon'     : 'needs_xon_xoff'            , 'oc'       : 'orig_colors'
  , 'op'       : 'orig_pair'                , 'orc'      : 'output_res_char'           , 'orhi'     : 'output_res_horz_inch'
  , 'orl'      : 'output_res_line'          , 'orvi'     : 'output_res_vert_inch'      , 'os'       : 'over_strike'
  , 'pad'      : 'pad_char'                 , 'pairs'    : 'max_pairs'                 , 'pause'    : 'fixed_pause'
  , 'pb'       : 'padding_baud_rate'        , 'pctrm'    : 'pc_term_options'           , 'pfkey'    : 'pkey_key'
  , 'pfloc'    : 'pkey_local'               , 'pfx'      : 'pkey_xmit'                 , 'pfxl'     : 'pkey_plab'
  , 'pln'      : 'plab_norm'                , 'porder'   : 'order_of_pins'             , 'prot'     : 'enter_protected_mode'
  , 'pulse'    : 'pulse'                    , 'qdial'    : 'quick_dial'                , 'rbim'     : 'stop_bit_image'
  , 'rc'       : 'restore_cursor'           , 'rcsd'     : 'stop_char_set_def'         , 'rep'      : 'repeat_char'
  , 'reqmp'    : 'req_mouse_pos'            , 'rev'      : 'enter_reverse_mode'        , 'rf'       : 'reset_file'
  , 'rfi'      : 'req_for_input'            , 'ri'       : 'scroll_reverse'            , 'rin'      : 'parm_rindex'
  , 'ritm'     : 'exit_italics_mode'        , 'rlm'      : 'exit_leftward_mode'        , 'rmacs'    : 'exit_alt_charset_mode'
  , 'rmam'     : 'exit_am_mode'             , 'rmclk'    : 'remove_clock'              , 'rmcup'    : 'exit_ca_mode'
  , 'rmdc'     : 'exit_delete_mode'         , 'rmicm'    : 'exit_micro_mode'           , 'rmir'     : 'exit_insert_mode'
  , 'rmkx'     : 'keypad_local'             , 'rmln'     : 'label_off'                 , 'rmm'      : 'meta_off'
  , 'rmp'      : 'char_padding'             , 'rmpch'    : 'exit_pc_charset_mode'      , 'rmsc'     : 'exit_scancode_mode'
  , 'rmso'     : 'exit_standout_mode'       , 'rmul'     : 'exit_underline_mode'       , 'rmxon'    : 'exit_xon_mode'
  , 'rs1'      : 'reset_1string'            , 'rs2'      : 'reset_2string'             , 'rs3'      : 'reset_3string'
  , 'rshm'     : 'exit_shadow_mode'         , 'rsubm'    : 'exit_subscript_mode'       , 'rsupm'    : 'exit_superscript_mode'
  , 'rum'      : 'exit_upward_mode'         , 'rwidm'    : 'exit_doublewide_mode'      , 's0ds'     : 'set0_des_seq'
  , 's1ds'     : 'set1_des_seq'             , 's2ds'     : 'set2_des_seq'              , 's3ds'     : 'set3_des_seq'
  , 'sam'      : 'semi_auto_right_margin'   , 'sbim'     : 'start_bit_image'           , 'sc'       : 'save_cursor'
  , 'scesa'    : 'alt_scancode_esc'         , 'scesc'    : 'scancode_escape'           , 'sclk'     : 'set_clock'
  , 'scp'      : 'set_color_pair'           , 'scs'      : 'select_char_set'           , 'scsd'     : 'start_char_set_def'
  , 'sdrfq'    : 'enter_draft_quality'      , 'setab'    : 'set_a_background'          , 'setaf'    : 'set_a_foreground'
  , 'setb'     : 'set_background'           , 'setcolor' : 'set_color_band'            , 'setf'     : 'set_foreground'
  , 'sgr'      : 'set_attributes'           , 'sgr0'     : 'exit_attribute_mode'       , 'sgr1'     : 'set_a_attributes'
  , 'sitm'     : 'enter_italics_mode'       , 'slength'  : 'set_pglen_inch'            , 'slines'   : 'set_page_length'
  , 'slm'      : 'enter_leftward_mode'      , 'smacs'    : 'enter_alt_charset_mode'    , 'smam'     : 'enter_am_mode'
  , 'smcup'    : 'enter_ca_mode'            , 'smdc'     : 'enter_delete_mode'         , 'smgb'     : 'set_bottom_margin'
  , 'smgbp'    : 'set_bottom_margin_parm'   , 'smgl'     : 'set_left_margin'           , 'smglp'    : 'set_left_margin_parm'
  , 'smglr'    : 'set_lr_margin'            , 'smgr'     : 'set_right_margin'          , 'smgrp'    : 'set_right_margin_parm'
  , 'smgt'     : 'set_top_margin'           , 'smgtb'    : 'set_tb_margin'             , 'smgtp'    : 'set_top_margin_parm'
  , 'smicm'    : 'enter_micro_mode'         , 'smir'     : 'enter_insert_mode'         , 'smkx'     : 'keypad_xmit'
  , 'smln'     : 'label_on'                 , 'smm'      : 'meta_on'                   , 'smpch'    : 'enter_pc_charset_mode'
  , 'smsc'     : 'enter_scancode_mode'      , 'smso'     : 'enter_standout_mode'       , 'smul'     : 'enter_underline_mode'
  , 'smxon'    : 'enter_xon_mode'           , 'snlq'     : 'enter_near_letter_quality' , 'snrmq'    : 'enter_normal_quality'
  , 'spinh'    : 'dot_horz_spacing'         , 'spinv'    : 'dot_vert_spacing'          , 'sshm'     : 'enter_shadow_mode'
  , 'ssubm'    : 'enter_subscript_mode'     , 'ssupm'    : 'enter_superscript_mode'    , 'subcs'    : 'subscript_characters'
  , 'sum'      : 'enter_upward_mode'        , 'supcs'    : 'superscript_characters'    , 'swidm'    : 'enter_doublewide_mode'
  , 'tbc'      : 'clear_all_tabs'           , 'tone'     : 'tone'                      , 'tsl'      : 'to_status_line'
  , 'u0'       : 'user0'                    , 'u1'       : 'user1'                     , 'u2'       : 'user2'
  , 'u3'       : 'user3'                    , 'u4'       : 'user4'                     , 'u5'       : 'user5'
  , 'u6'       : 'user6'                    , 'u7'       : 'user7'                     , 'u8'       : 'user8'
  , 'u9'       : 'user9'                    , 'uc'       : 'underline_char'            , 'ul'       : 'transparent_underline'
  , 'vpa'      : 'row_address'              , 'vt'       : 'virtual_terminal'          , 'wait'     : 'wait_tone'
  , 'widcs'    : 'wide_char_size'           , 'wind'     : 'set_window'                , 'wingo'    : 'goto_window'
  , 'wnum'     : 'maximum_windows'          , 'wsl'      : 'width_status_line'         , 'xenl'     : 'eat_newline_glitch'
  , 'xhp'      : 'ceol_standout_glitch'     , 'xhpa'     : 'col_addr_glitch'           , 'xmc'      : 'magic_cookie_glitch'
  , 'xoffc'    : 'xoff_character'           , 'xon'      : 'xon_xoff'                  , 'xonc'     : 'xon_character'
  , 'xsb'      : 'no_esc_ctlc'              , 'xt'       : 'dest_tabs_magic_smso'      , 'xvpa'     : 'row_addr_glitch'
  , 'zerom'    : 'zero_motion'
  }


##################################################
#                                                #
##################################################
def _make_variable_slots() :

  slots = {}
  for i in range(26) :
    slots[ chr( ord('a') + i ) ] = i
    slots[ chr( ord('A') + i ) ] = i+26

  return FrozenDict(slots)

VARIABLE_SLOTS = _make_variable_slots()
