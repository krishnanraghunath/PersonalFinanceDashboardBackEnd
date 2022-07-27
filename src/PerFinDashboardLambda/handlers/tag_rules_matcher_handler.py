from PerFinDashboardLambda.processors.tag_rules_processors.tag_rules_processor import TagRulesProcessor

def TagRulesMatcherHandler(event,context):
     tagRulesProcessor = TagRulesProcessor()
     for record in event['Records']:
          if record['eventName'] in ['INSERT','MODIFY']:
               new_image = record['dynamodb']['NewImage']
               for key in new_image:
                    try:
                         new_image[key] = new_image[key]['S']
                    except:
                         new_image[key] = int(float(new_image[key]['N']))
               tagRulesProcessor.process_entry(new_image)
     tagRulesProcessor.tagTransactionsTableClient.batch_write_items(True)




