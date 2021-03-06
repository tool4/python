<h1></h1>
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
          var data = google.visualization.arrayToDataTable([
<?php
          $csv_file = $_GET["csv_file"];
          $file_index = $_GET["file_index"];
          $col_with_data = $_GET["col"];
          $row = 1;
          if (($handle = fopen($csv_file, "r")) !== FALSE)
          {
              $row = 0;
              while (($data = fgetcsv($handle, 1000, ",")) !== FALSE)
              {
                  $num = count($data);
                  if ($row % 6 == 0 || $row == 1)
                  {
                      echo "\n\t\t\t\t";
                  }
                  echo " [";
                  for ($c=0; $c < $num; $c++)
                  {
                      $entry = trim($data[$c]);
                      if ($data[$c] && ($c == $col_with_data || $c == 0))
                      {
                          if ($row == 0)
                              $title =  $entry;
                          if ($row > 0 and $c > 0)
                              echo $entry;
                          else
                              echo "'" . $entry . "'";
                          if ($c < $num - 2)
                              echo ", ";
                      }
                  }
                  echo "],";
                  $row=$row +1;
              }
              fclose($handle);
          }
          else
          {
              echo "Cannot open file: " . $csv_file;
          }
          ?>
          ]);

          var options = {
<?php
              $name = $_GET["name"];
              $name = $csv_file;
              $name = str_replace(".csv", "", $name);
              $name = str_replace("netinfo", "", $name);
              $name = str_replace("temp", "", $name);
              $name = $title . " " . $name;
              $name = str_replace("_", " ", $name);
              if($name != "")
                  echo "\t\t\t\ttitle: '" . $name . "'";
              else
                  echo "\t\t\t\ttitle: 'Chart'";
?>,
                curveType: 'function',
                legend: { position: 'bottom' },
                //vAxis:  { minValue: 0 },
                explorer: { axis: 'horizontal', keepInBounds: true, maxZoomIn: 4.0 }
          };
          var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
          chart.draw(data, options);
      }
    </script>
<?php
$files = scandir(".");
$total = count($files);
for($x = 0; $x <= $total; $x++)
{
    $ext = substr($files[$x], -3, 3);
    if ($ext == "csv")
    {
        $csv_files_array[] = $files[$x];
        ++$csv_index;
    }
}

$next_file = intval($file_index);
$col = $col_with_data;
$next_col = $col;
?>
    <script type="text/javascript">
        function KeyPress (event){
            var chCode = ('charCode' in event) ? event.charCode : event.keyCode;
            var url = window.location.href;
            var pos = url.lastIndexOf("/") + 1;
            url = url.substring(0, pos);
            //alert(url);
            var reload = false;
            var nextfile = <?php echo intval($file_index); ?>;
            var nextcol = <?php echo intval($col); ?>;

            //alert ("The Unicode character code is: " + chCode);
            if(chCode == 100)
            {
                <?php
                $next_file = intval($file_index) + 1;
                if ($next_file >= $csv_index)
                    $next_file = 0;
                $url = "readcsv.php?csv_file=".
                     $csv_files_array[$next_file].
                     "&col=".$next_col."&name=".
                     $title.
                     "&file_index=".
                     $next_file;
                echo 'url = url + "' . $url . '";';
                ?>
                reload = true;
            }
            if(chCode == 97)
            {
                <?php
                $next_file = intval($file_index) - 1;
                if ($next_file < 0)
                    $next_file = $csv_index -1;
                $url = "readcsv.php?csv_file=" .
                     $csv_files_array[$next_file] .
                     "&col=".$next_col."&name=" .
                     $title .
                     "&file_index=" .
                     $next_file;
                echo 'url = url + "' . $url . '";';
                ?>
                reload = true;
            }
            if(chCode == 119)
            {
                <?php
                $next_file = intval($file_index);
                $next_col = $col + 1;
                if ($next_col > 3)
                    $next_col = 1;
                $url = "readcsv.php?csv_file=".
                     $csv_files_array[$next_file].
                     "&col=".$next_col."&name=".
                     $title.
                     "&file_index=".
                     $next_file;
                echo 'url = url + "' . $url . '";';
                ?>
                reload = true;
            }
            if(chCode == 115)
            {
                <?php
                $next_file = intval($file_index);
                $next_col = $col - 1;
                if ($next_col < 1)
                    $next_col = 3;
                $url = "readcsv.php?csv_file=".
                     $csv_files_array[$next_file].
                     "&col=".$next_col."&name=".
                     $title.
                     "&file_index=".
                     $next_file;
                echo 'url = url + "' . $url . '";';
                ?>
                reload = true;
            }

            if (reload)
            {
                <?php
                ?>
                window.open(url,"_self");
                //window.location(url);
            }

        }
    </script>
</head>
  <body  onkeypress="KeyPress(event);">
    <div id="curve_chart" style="width: 100%; height: 100%"></div>
  </body>
</html>


<?php
$csv_file = $_GET["csv_file"];
echo $csv_file;
$row = 1;
if (($handle = fopen($csv_file, "r")) !== FALSE)
{
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE)
    {
        $num = count($data);
        echo "<br/>\n\t[";
        $row++;
        for ($c=0; $c < $num; $c++) {
            if ($data[$c])
                echo "'" . $data[$c] . "'";
            if ($c < $num - 2)
                echo ", ";
        }
        echo "],";
    }
    fclose($handle);
}
?>
