<?php
foreach (\Drupal::entityTypeManager()->getStorage('commerce_product_variation')->loadMultiple() as $variation) {
  if (!$variation->getProduct()) {
    $variation->delete();
  }
}

$entityTypeManager = \Drupal::entityTypeManager()->getStorage('commerce_product');
    $ids = $entityTypeManager->getQuery()->execute();
    foreach(array_chunk($ids, 100) as $pids) {
      $entitys = $entityTypeManager->loadMultiple($pids);
      foreach($entitys as $entity) {
          $entity->set('variations', []);
          $entity->delete();
      }
    }

