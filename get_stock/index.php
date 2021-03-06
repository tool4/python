<?php

function DEBUG($msg_string)
{
    //    echo $msg_string;
}

$files = scandir(".");
$total = count($files);
$images = array();
$csv_index = 0;
$file_index = $_GET["file_index"];
for($x = 0; $x <= $total; $x++)
{
    $ext = substr($files[$x], -3, 3);
    if ($ext == "csv")
    {
        if ($files[$x] != '.' && $files[$x] != '..')
        {
            $images[] = $files[$x];
            $title = substr($files[$x], 0, -4);
            $paragraphs[$x] = "<a style=\"display:inline-block;width:800px\" href=".
                            "readcsv.php?csv_file=".
                            $files[$x].
                            "&col=1&name=".
                            $title.
                            "&file_index=".
                            $csv_index.
                            ">".
                            $files[$x].
                            " </a> ".
                            number_format(filesize($files[$x])/1024, 2, '.', '').
                            " KB <br>\n";
        }
        $csv_files_array[] = $files[$x];
        ++$csv_index;
    }
    else
    {
        $paragraphs[$x] = "<a style=\"display:inline-block;width:800px\" href=".
                        $files[$x].
                        ">".
                        $files[$x].
                        " </a> ".
                        number_format(filesize($files[$x])/1024, 2, '.', '').
                        " KB <br>\n";
    }
}

DEBUG( "csv_index: ". $csv_index. "<BR>\n");
DEBUG(  "file_index: ". $file_index. "<BR>\n");

if (intval($file_index) > $csv_index)
    $file_index = "0";

if ($file_index != "" && intval($file_index) <= intval($csv_index))
{
    DEBUG( "total files: " . $total . "\n");
    DEBUG( "csv files: " . $total . "\n");
    for($c = 0; $c <= $csv_index; $c++)
        DEBUG( $csv_files_array[$c] . "\n");

    $uri = $_SERVER['REQUEST_URI'];
    DEBUG( $uri . "\n");

    $protocol = ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] != 'off') ||
                 $_SERVER['SERVER_PORT'] == 443) ? "https://" : "http://";

    $url = $protocol . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
    DEBUG( $url . "\n");

    $offset = strrpos($url, "/");
    DEBUG( "last / at: " .$offset . "\n");

    $url = substr($url, 0, $offset);
    DEBUG( $url . "\n");

    $title = substr($csv_files_array[$file_index], 0, -4);

    $url = $url . "/readcsv.php?csv_file=" . $csv_files_array[$file_index] . "&col=1&name=" .
         $title . "&file_index=" . $file_index;

    DEBUG( "\n" . $url);
    #$url = "http://www.google.com";
    echo '
<!DOCTYPE html>
<html>
    <head>
        <title>Local weather files</title>
        <meta http-equiv = "refresh" content="0;url='.$url.'" />
<!--    <meta http-equiv = "refresh" content="5;url=http://example.com/" /> -->
    </head>
    <body>
        <p>Hello HTML5!</p>
';

    for ($p=0; $p<$csv_index; $p++)
    {
        echo "\t\t" . $paragraphs[$p];
    }

    echo '<br>
    </body>
</html>


';
}
else
{
    #echo "File index is: ", intval($file_index), "<BR>\n";
    for ($p=0; $p<$total; $p++)
    {
        echo "\t\t" . $paragraphs[$p];
    }
}
?>
