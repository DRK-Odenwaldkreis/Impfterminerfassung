<?php

/* **************

Websystem für das Testzentrum DRK Odenwaldkreis
Author: Marc S. Duchene
March 2021

** ************** */

include_once 'preload.php';
if( isset($GLOBALS['G_sessionname']) ) { session_name ($GLOBALS['G_sessionname']); }
session_start();
$sec_level=1;
$current_site="log";

// Include functions
include_once 'tools.php';
include_once 'auth.php';
include_once 'menu.php';

// role check
if( A_checkpermission(array(0,0,0,4,0)) ) {


    // Print html header
    echo $GLOBALS['G_html_header'];

    // Print html menu
    echo $GLOBALS['G_html_menu'];
    echo $GLOBALS['G_html_menu2'];

    // Print html content part A
    echo $GLOBALS['G_html_main_right_a'];

    echo '<h1>Logs</h1>';

    echo '<pre>UID: '.$_SESSION['uid'].'</pre>';


    // tail of $file with last $int lines
    function file_tail($file,$int) {
        $file_content=file($file);
        $r="";
        for ($i = max(0, count($file_content)-$int-1); $i < count($file_content); $i++) {
            $r .= $file_content[$i] . "";
        }
        return $r;
    }

    //Get log file
    $log_path="/home/webservice/Logs/";
    $log_array=scandir($log_path);
    foreach($log_array as $a) {
        if(!($a=="." || $a=="..")) {
            echo '<h3>'.$a.'</h3>';
            echo '<pre>';
            echo file_tail($log_path.$a,40);
            echo '</pre>';
        }
    }


} else {
    // Print html header
    echo $GLOBALS['G_html_header'];

    // Print html menu
    echo $GLOBALS['G_html_menu'];
    echo $GLOBALS['G_html_menu2'];

    // Print html content part A
    echo $GLOBALS['G_html_main_right_a'];
    echo '<h1>KEINE BERECHTIGUNG</h1>';
}


// Print html content part C
echo $GLOBALS['G_html_main_right_c'];
// Print html footer
echo $GLOBALS['G_html_footer'];

?>