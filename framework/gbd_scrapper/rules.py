from database import db_configuration
class RuleEmptyError(Exception):
    def __init__(self):
        pass

# definitions = {
#     "product_name": {
#         "selector": "css",
#         "alias": "div.product-name > h1",
#         "default_value":"not available"
#     },
#     "std": {
#         "selector": "css",
#         "alias": "div.std",
#         "default_value":"not available"
#     },
#     "product_sku":{
#         "selector": "regex",
#         "alias": "SKU(.*?)</p>",
#         "default_value": "no sku"
#     }
# }
# print definitions

import mysql.connector

class RuleGenerator:

    @staticmethod
    def generate(domain_name):
        


        try:
            cnx = mysql.connector.connect(**db_configuration)

            cursor = cnx.cursor()

            query = ("SELECT s.DomainName, ssk.SiteId, ssk.ScrapeScheme, ssk.KeyName, ssk.KeyAlias, "
                     "ssk.KeyDefaultValue, ssk.CreateDate, ssk.CreateUser, ssk.UpdateDate, ssk.UpdateUser "
                     "FROM `SiteScrapeKey` ssk INNER JOIN Site s ON ssk.SiteId = s.Id "
                     # "WHERE ssk.SiteId IN (%(SiteId)s)")
                     "WHERE s.DomainName Like \"%{}%\"".format(domain_name))

            cursor.execute(query)

            rules = []
            for (domain_name, site_id, selector, alias, column_title,default_value,create_date, create_user,
                 update_date, update_user) in cursor:
                dictionary = {
                    column_title: {
                        "selector": selector,
                        "alias": alias,
                        "default_value":default_value
                    }
                }

                rules.append(dictionary)

            # print cursor._executed  # Uncomment it to see the raw query being executed in the mysql
            if len(rules) > 0:
                cursor.close()
                cnx.close
                return rules
            else:
                raise RuleEmptyError
        except Exception as e:
            # print cursor._executed
            raise e

if __name__=="__main__":
    # rules = RuleGenerator.generate("exam.ioe.edu.np")
    rules = RuleGenerator.generate("www.amazon.com")
    print rules
            # From domain name get the site id