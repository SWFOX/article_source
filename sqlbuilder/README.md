SqlBuilder 为构造 SQL 语句的链式操作类

操作

```
$SqlBuilder = new SqlBuilder('TABLE_A');

var_dump($SqlBuilder
    ->select(array('id','name', 'age'))
    ->where('\'id\'>2')
    ->limit(10,10)
    ->order('`age` DESC')
    ->make()
);PHP_EOL;

var_dump($SqlBuilder
    ->delete()
    ->where(array('name'=>'A'))
    ->make()
);PHP_EOL;

var_dump($SqlBuilder
    ->add(array('id' => 16, 'name'=>'H', 'age'=>15))
    ->make()
);PHP_EOL;

var_dump($SqlBuilder
    ->update(array('name'=>'A', 'age'=>15))
    ->where(array('id'=>'1'))
    ->make()
);PHP_EOL;

var_dump($SqlBuilder
    ->select()
    ->join('`TABLE_B` ON `TABLE_A.id`=`TABLE_B.id`')
    ->group('`TABLE_B.name`')->make()
);PHP_EOL;
```

结果

```
array(2) {
  ["option"]=>
  array(2) {
    ["mode"]=>
    string(1) "r"
    ["table"]=>
    string(7) "TABLE_A"
  }
  ["sql"]=>
  string(83) "SELECT `id`,`name`,`age` FROM `TABLE_A` WHERE 'id'>2 ORDER BY `age` DESC LIMIT 10, 10"
}
array(2) {
  ["option"]=>
  array(2) {
    ["mode"]=>
    string(1) "r"
    ["table"]=>
    string(7) "TABLE_A"
  }
  ["sql"]=>
  string(40) "DELETE FROM `TABLE_A` WHERE `name` = 'A'"
}
array(2) {
  ["option"]=>
  array(2) {
    ["mode"]=>
    string(1) "w"
    ["table"]=>
    string(7) "TABLE_A"
  }
  ["sql"]=>
  string(64) "INSERT INTO `TABLE_A` (`id`, `name`, `age`) VALUES (16, 'H', 15)"
}
array(2) {
  ["option"]=>
  array(2) {
    ["mode"]=>
    string(1) "w"
    ["table"]=>
    string(7) "TABLE_A"
  }
  ["sql"]=>
  string(58) "UPDATE `TABLE_A` set `name`='A', `age`=15 WHERE `id` = '1'"
}
array(2) {
  ["option"]=>
  array(2) {
    ["mode"]=>
    string(1) "r"
    ["table"]=>
    string(7) "TABLE_A"
  }
  ["sql"]=>
  string(97) "SELECT * FROM `TABLE_A` INNER JOIN `TABLE_B` ON `TABLE_A.id`=`TABLE_B.id` GROUP BY `TABLE_B.name`"
}
```