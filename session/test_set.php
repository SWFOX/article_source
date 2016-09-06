<?php 

include './MySession.php';

$session = new MySession();

$session->set('name', 'xiaoming');
$session->set('age', 22);
$session->set('isadmin', true);
$session->save();

echo 'OK';