<?php

require_once './vendor/autoload.php';
require_once './config.php';

use Pagination\Pagination;
use Pagination\StrategySimple;

if (isset($_GET['page']) && is_numeric($_GET['page'])) {
    $page = $_GET['page'];
} else {
    $page = 1;
}
// count
$keyWord = isset($_REQUEST['keyWord']) ? trim($_REQUEST['keyWord']) : null;
$remove = isset($_REQUEST['remove']) ? trim($_REQUEST['remove']) : null;
$countSql = "SELECT COUNT(*) FROM jkf ";
if ($remove || $keyWord) {
    $countSql .= ' WHERE ';
    $query = '';
    if ($keyWord) {
        $query .= "content like '%$keyWord%' AND ";
    }
    if ($remove) {
        $query .= "content not like '%$remove%' AND ";
    }
    $query = rtrim($query, " AND ");
    $countSql .= $query;
}

$totalNum = $dbConn->fetchColumn($countSql);
if (!$totalNum) {
    exit('沒有資料!');
}

//use pagination class with results, per page and page
$perNum = 15;
$pagination = new Pagination($totalNum, $perNum, $page);
//get indexes in page
$indexes = $pagination->getIndexes(new StrategySimple($perNum));
$iterator = $indexes->getIterator();
//get all indexes
$all = $pagination->getAllIndexesOfPages();
$iteratorAll = $all->getIterator();

// page
$sql = "SELECT * FROM jkf ";
if ($remove || $keyWord) {
    $sql .= ' WHERE ';
    $query = '';
    if ($keyWord) {
        $query .= "content like '%$keyWord%' AND ";
    }
    if ($remove) {
        $query .= "content not like '%$remove%' AND ";
    }
    $query = rtrim($query, " AND ");
    $sql .= $query;
}
$offsetStart = $perNum * $page - $perNum;
$sql .= " order by id limit {$offsetStart},{$perNum}";

$res = $dbConn->fetchRowMany($sql);

// ===========html=============
include 'header.html';
?>
<div class="row">
    <div class="col-md-12">
        <div class="page-header">
            <h1>老司機最懂你
                <small>現在第: <?php echo $page; ?>頁</small>
                <span class="label label-info"> 總共: <?php echo $pagination->getTotalOfPages(); ?>頁</span>
                <span class="label label-info"> 總共: <?php echo $totalNum; ?>筆</span>
            </h1>
        </div>
    </div>
</div>
<form action="/" method="post">
  <div class="form-group">
    <label for="keyWord">關鍵字</label>
    <input type="text" class="form-control" id="keyWord" placeholder="吹...刪除可全搜" name="keyWord" value="<?php if ($keyWord) {echo $keyWord;}?>">
  </div>
  <div class="form-group">
    <label for="remove">排除</label>
    <input type="text" class="form-control" id="remove" placeholder="西門彤彤..." name="remove" value="<?php if ($remove) {echo $remove;}?>">
  </div>
  <button type="submit" class="btn btn-primary">提交</button>
</form>
<hr>
<div class="row">
    <div class="col-md-9">

        <div class="row">
            <div class="col-md-10">
                <p><strong>結果:</strong></p>
            </div>
        </div>
        <table class="table table-striped">
            <thead >
                <tr>
                <th scope="col">id</th>
                <th scope="col">頭像</th>
                <th scope="col">標題</th>
                <th scope="col">連結</th>
                <th scope="col">內文</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($res as $v) {?>
                    <tr>
                    <th scope="row"><?php echo $v['id'] ?></th>
                    <td><img src="<?php echo $v['avatar'] ?>"></td>
                    <td><?php echo $v['title'] ?></td>
                    <td><a href="<?php echo $v['url'] ?>" target="_blank"><?php echo $v['url'] ?></a></td>
                    <td><?php echo $v['content'] ?></td>
                    </tr>
                <?php }?>
            </tbody>
        </table>
        <br>
        <span style="color:darkred">!!!!有打關鍵字不要按前後，只能按數字</span>
        <br>
        <div class="row">
            <div class="col-md-10">
                <nav aria-label="Page navigation">
                    <ul class="pagination">
                        <li>
                            <a href="?page=<?php echo $pagination->getFirstPage(); ?>" aria-label="First">
                                <span aria-hidden="true">First</span>
                            </a>
                        </li>
                        <li>
                            <a href="?page=<?php echo $pagination->getPreviousPage(); ?>" aria-label="Previous">
                                <span aria-hidden="true">&laquo;</span>
                            </a>
                        </li>
                        <?php while ($iterator->valid()): ?>
                            <li>
                                <a href="?page=<?php echo $iterator->current() ?>&keyWord=<?php if ($keyWord) {echo $keyWord;}?>&remove=<?php if ($remove) {echo $remove;}?>" class="xxx">
                                    <?php echo $iterator->current() ?>
                                </a>
                            </li>
                        <?php $iterator->next();endwhile;?>
                        <li>
                            <a href="?page=<?php echo $pagination->getNextPage(); ?>" aria-label="Next">
                                <span aria-hidden="true">&raquo;</span>
                            </a>
                        </li>
                        <li>
                            <a href="?page=<?php echo $pagination->getLastPage(); ?>" aria-label="Last">
                                <span aria-hidden="true">Last</span>
                            </a>
                        </li>
                    </ul>
                </nav>
            </div>
        </div>
    </div>
</div>
