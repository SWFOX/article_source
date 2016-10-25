<?php
/**
 * User: qiming.c <qiming.c@foxmail.com>
 * Date: 2016/10/25
 * Time: 21:00
 */

class SqlBuilder
{
    protected $_error  = '';
    protected $_where  = '';
    protected $_order  = '';
    protected $_limit  = '';
    protected $_select = '';
    protected $_insert = '';
    protected $_update = '';
    protected $_table  = '';
    protected $_group  = '';
    protected $_delete = '';
    protected $_count  = '';
    protected $_join   = '';

    public function __construct($table)
    {
        $this->_table = "`".$table."`";
    }

    /**
     *
     * @access public
     * @param  mixed $where
     * @return $this
     * @example  where("name='A'") Or where(array('id'=>'1', 'name'=>'A'))
     * 对于 array 参数暂时只支持 AND 类型拼接。
     */
    public function where($where="1=1")
    {
        if (is_string($where)) {
                $this->_where = " WHERE ".$where;

        } else if (is_array($where)) {
            $this->_where = " WHERE";
            self::checkArrayVal($where);
            foreach ($where as $key => $value) {
                $this->_where .= " `$key` = ".$value." AND";
            }
            //删去最后多余的" AND"，这里用了strlen，如果where中带有中文长度可能不准确
            $this->_where = substr($this->_where,0,strlen($this->_where)-4);

        } else {
            $this->_where = '';
        }
        return $this;
    }

    public function order($order="id DESC")
    {
        $this->_order = " ORDER BY ".$order;
        return $this;
    }

    public function limit($offset="20", $length=null)
    {
        if ($length) {
            $this->_limit = " LIMIT ".$offset.", ".$length;
        } else {
            $this->_limit = " LIMIT 0, ".$offset;
        }
        return $this;
    }

    /**
     * @param  mixed $select
     * @example  select(array('id', 'name', 'age') Or select("id, name, age")
     * @return $this
     */
    public function select($select="*")
    {
        if (is_array($select)) {
            //为参数加上``
            $select = array_map(function($se){return '`'.$se.'`,';}, $select);
            if (empty($select)) $select=array('*');
            $this->_select = "SELECT ".rtrim(implode($select), ',')." FROM ".$this->_table;

        } elseif ($select == '*') {
            $this->_select = "SELECT ".$select." FROM ".$this->_table;

        //如果 $select 类型为 string
        } else {
            $selectArray = explode(',', $select);
            $selectArray = array_map('trim', $selectArray);
            $select = '`'.implode('`, `', $selectArray).'`';
            if (empty($select)) $select='*';
            $this->_select = "SELECT ".$select." FROM ".$this->_table;
        }
        return $this;
    }

    /**
     * @param  array $value
     * @example  add(array('id' => 1, 'name'=>'H', 'age'=>15))
     * @return $this
     */
    public function add($value=array())
    {
        $this->_insert = "INSERT INTO $this->_table";
        self::checkArrayVal($value);
        $this->_insert .= " (`".implode('`, `', array_keys($value))."`) VALUES (".implode(', ', array_values($value)).")";
        return $this;
    }

    /**
     * @param  array $value
     * @example  update(array('name'=>'A', 'age'=>15))
     * @return $this
     */
    public function update($value = array())
    {
        $this->_update = "UPDATE $this->_table set";
        self::checkArrayVal($value);
        foreach ($value as $key => $val) {
            $this->_update .= " `$key`=".$val.",";
        }
        $this->_update = rtrim($this->_update, ',');
        return $this;
    }

    public function group($group)
    {
        $this->_group = " GROUP BY ".$group;
        return $this;
    }

    /**
     * @example  delete()->where('id=1')
     * @return $this
     */
    public function delete()
    {
        $this->_delete = "DELETE "."FROM ".$this->_table;
        return $this;
    }

    /**
     * @example $Object->count()->where()->buildSql()
     * @return $this
     * @todo 统计语句
     */
    public function count($count='*')
    {
        $this->_count = 'SELECT COUNT('.$count.') FROM '.$this->_table;
        return $this;
    }

    /**
     * @param $join
     * @param $style
     * @example $Object->select()->join('TABLE ON ...')->buildSql()
     * @return $this
     * 跨表操作
     */
    public function join($join, $style='INNER')
    {
        $this->_join = ' '.$style.' JOIN '.$join;
        return $this;
    }

    /** 简单检测sql语句有没有明显错误 */
    protected function checkSql()
    {
        if ($this->_select && $this->_update) {
            $this->_error.="Error:不能同时使用select和update ";
        } elseif ($this->_select && $this->_insert) {
            $this->_error.="Error:不能同时使用select和add ";
        } elseif ($this->_select && $this->_delete) {
            $this->_error.="Error:不能同时使用select和delete ";
        } elseif ($this->_update && $this->_insert) {
            $this->_error.="Error:不能同时使用update和add ";
        } elseif ($this->_delete && $this->_update) {
            $this->_error.="Error:不能同时使用update和delete ";
        } elseif ($this->_insert && $this->_delete) {
            $this->_error.="Error:不能同时使用insert和delete ";
        }
    }

    /**
     * @return array('sql'=>sql语句, 'option'=>array('mode'=>读写类型, 'table'=>表名))
     * 构建sql语句
     */
    public function make()
    {
        $sql = $this->buildSql();
        if (preg_match('/INSERT/i', $sql) || preg_match('/UPDATE/i', $sql)) {
            $return['option']['mode'] = 'w';
        } else {
            $return['option']['mode'] = 'r';
        }
        $return['option']['table'] = trim($this->_table, '`');
        $return['sql'] = $sql;
        return $return;
    }

    /** 构建 sql 语句 */
    protected function buildSql()
    {
        $this->checkSql();
        $sql = null;
        if ($this->_error) {
            trigger_error($this->_error);
            $this->resetargs();
            return $sql;
        } elseif ($this->_select) {
            $sql =  $this->_select.$this->_join.$this->_where.$this->_group.$this->_order.$this->_limit;
        } elseif($this->_update) {
            $sql =  $this->_update.$this->_where;
        } elseif($this->_insert) {
            $sql = $this->_insert;
        } elseif ($this->_delete) {
            $sql = $this->_delete.$this->_where;
        } elseif ($this->_count) {
            $sql = $this->_count.$this->_join.$this->_where;
        }
        $this->resetArgs();
        return $sql;
    }

    /** 重置参数 */
    protected function resetArgs()
    {
        $this->_where  = '';
        $this->_order  = '';
        $this->_limit  = '';
        $this->_select = '';
        $this->_update = '';
        $this->_insert = '';
        $this->_group  = '';
        $this->_delete = '';
        $this->_error  = '';
        $this->_count  = '';
        $this->_join   = '';
    }

    /**
     * @param $array
     * @return array
     * 对array参数进行处理,主要是对字符串加上''
     */
    protected static function checkArrayVal(&$array=array())
    {
        foreach ($array as $key => &$val) {
            if (is_string($val)) {
                $val = '\''.$val.'\'';
            }
        }
    }

}