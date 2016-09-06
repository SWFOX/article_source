<?php 

include './MySession.php';

$session = new MySession();

echo $session->get('name') . ' ' . $session->get('age'). ' ' .$session->get('isadmin');