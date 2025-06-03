from database.DB_connect import DBConnect
from model.order import Order


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getStores():
        cnx=DBConnect.get_connection()
        res=[]
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor=cnx.cursor(dictionary=True)
            query="""select s.store_id as s
                    from stores s """
            cursor.execute(query,)
            for row in cursor:
                res.append(row["s"])
            cursor.close()
            cnx.close()
        return res

    @staticmethod
    def getNodes(store):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                    from orders o 
                    where o.store_id = %s"""
            cursor.execute(query,(store,) )
            for row in cursor:
                res.append(Order(**row))
            cursor.close()
            cnx.close()
        return res

    @staticmethod
    def getEdges(store,idMap,giorni):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select o1.order_id as id1, o2.order_id as id2,(oi2.quantity+oi.quantity) as peso
                    from orders o1, orders o2, order_items oi, order_items oi2 
                    where o1.store_id = %s
                    and o2.store_id = o1.store_id
                    and o2.order_id <> o1.order_id
                    and o1.order_date<o2.order_date 
                    and o2.order_date between o1.order_date and date_add(o1.order_date, interval %s day)
                    and o1.order_id=oi.order_id
                    and o2.order_id =oi2.order_id """
            cursor.execute(query, (store, giorni))
            for row in cursor:
                if row["id1"] in idMap and row["id2"] in idMap:
                    res.append((idMap[row["id1"]],idMap[row["id2"]],row["peso"]))
            cursor.close()
            cnx.close()
        return res