# Note

bitnami/elasticsearch not work on es ml feacture  and the eland ssl has some issue just without ssl first

# install nlp module to test
```
eland_import_hub_model --url  http://localhost:9200/ \
--hub-model-id elastic/distilbert-base-cased-finetuned-conll03-english --task-type ner
```

# how to use ? deploy module frist, minimum memory 4G for even es node
```
Deploy the model in your clusteredit
After you import the model and vocabulary, you can use Kibana to view and manage their deployment across your cluster under Machine Learning > Model Management. Alternatively, you can use the start trained model deployment API or specify the --start option when you run the eland_import_hub_model script.

Since eland uses APIs to deploy the models, you cannot see the models in Kibana until the saved objects are synchronized. You can follow the prompts in Kibana, wait for automatic synchronization, or use the sync machine learning saved objects API.

When you deploy the model, it is allocated to all available machine learning nodes. The model is loaded into memory in a native process that encapsulates libtorch, which is the underlying machine learning library of PyTorch.

You can set additional deployment options that affect the performance of the model. For example, specify the number of allocations and the threads per allocation to optimize the throughput and speed of inference requests in your production environment. For more information about these options, refer to the start trained model deployment API.
```
```
curl -X POST  localhost:9200/_ml/trained_models/elastic__distilbert-base-cased-finetuned-conll03-english/_infer  -H "Content-Type: application/json" -d '{
  "docs":[{"text_field": "Sasha bought 300 shares of Acme Corp in 2022."}]
}'

```

