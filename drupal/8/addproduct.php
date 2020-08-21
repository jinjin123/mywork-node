<?php
use Drupal\taxonomy\Entity\Term;
$store = \Drupal\commerce_store\Entity\Store::load(1);
$file = fopen("clear2.csv","r");
$i = 0;
while($data = fgetcsv($file,10000,";"))
{
        $i++;
        if($i==1)
        {
            continue;//过滤表头
        }
        if($data[0]!='')
        {
            $price = new \Drupal\commerce_price\Price($data[3], 'USD');
            $variation = \Drupal\commerce_product\Entity\ProductVariation::create([
              'type' => 'watch', 
              'sku' => $data[5], 
              'status' => 1,
              'price' => $price,
              'title' => $data[0],
              'attribute_color' => $red, 
            ]);

            $t = explode(",",$data[2]);
	    $tmp=array();
	    foreach($t as $value){
                       $b = str_replace("'","",$value);
                        $c = str_replace("u","",$b);
                        $d= str_replace ("[","",$c);
                        $e= str_replace ("]","",$d);
                        array_push($tmp,$e);
            };

           // foreach(explode(",",$data[2]) as $value ){
            //     array_push($tmp,$value );
           // }
	   $term = \Drupal::entityTypeManager()->getStorage('taxonomy_term')->loadByProperties(['name' => $data[0]]);
           $product = \Drupal\commerce_product\Entity\Product::create([
              'stores' => [$store],
              'variations' => [$variation],
              'uid' => 1,
              'type' => 'watch', 
              'title' => $data[4],
              'field_ask_price'=>$price,
              'field_bezel_material ' => $data[17],
              'field_case_back' => $data[19],
              'field_case_back_width' => $data[21],
              'field_case_band_color' => $data[25],
              'field_case_band_length' => $data[26],
              'field_case_band_material' => $data[23],
              'field_case_band_width' => $data[24],
              'field_case_diameter' => $data[14],
              'field_case_face' => $data[18],
              'field_case_number' => $data[22],
              'field_case_shape' => $data[20],
              'field_case_thickness' => $data[15],
              'field_case_weight' => $data[32],
              'field_cate' => $term,
              'field_cate_img' => $data[1],
              'field_clasp' => $data[27],
              'field_clasp_material' =>  $data[23],
              'field_crust_material' => $data[9],
              'body' => $data[31],
	       'field_extras' => $data[29],
               'field_manufacturer' => $data[11],
               'field_others' => $data[30],
               'field_power_time' => $data[12],
               'field_watch_sex' => $data[10],
               'field_shock' => $data[13],
               'field_sku' => $data[5],
               'field_watch_core' => $data[7],
               'field_watch_core_num' => $data[8],
               'field_watch_style' => $data[6],
               'field_water_resistance' => $data[16],
               'field_year' => $data[33],
               'field_detailimg' => $tmp,
            ]);
	    $product->save();
        }
}

fclose($file);
?>

