from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import uuid
import time
import os
import traceback, sys
import wallet_api
import mixin_asset_id_collection
import sqlalchemy
import mixin_sqlalchemy_type
import exincore_api
import oceanone_api
import base64
import datetime


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(object)
class Asset_addresses_Thread(QRunnable):
    def __init__(self, wallet_obj, asset_obj, *args, **kwargs):
        super(Asset_addresses_Thread, self).__init__()
        self.wallet_obj = wallet_obj
        self.asset_obj  = asset_obj
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.wallet_obj.get_asset_withdrawl_addresses(self.asset_obj.asset_id)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
        print("Withdraw address of asset Thread")


class AccountsSnapshots_Thread(QRunnable):
    def __init__(self, wallet_obj, starttime, delay_seconds = 0, *args, **kwargs):
        super(AccountsSnapshots_Thread, self).__init__()
        self.wallet_obj = wallet_obj
        self.starttime = starttime
        self.delay_seconds = delay_seconds
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            time.sleep(self.delay_seconds)
            result = self.wallet_obj.account_snapshots_after(self.starttime, "", 500)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
        print("Account snapshot Thread")

class ReadAsset_Info_Thread(QRunnable):
    def __init__(self, wallet_obj, asset_id , *args, **kwargs):
        super(ReadAsset_Info_Thread, self).__init__()
        self.wallet_obj = wallet_obj
        self.asset_id = asset_id
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.wallet_obj.get_singleasset_balance(self.asset_id)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
        print("ReadAsset_Info_Thread")


class Ocean_Thread(QRunnable):
    def __init__(self, base_asset_id, target_asset_id , delay_seconds = 0,  *args, **kwargs):
        super(Ocean_Thread, self).__init__()
        self.target_asset_id = target_asset_id
        self.base_asset_id = base_asset_id
        self.delay_seconds = delay_seconds
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            time.sleep(self.delay_seconds)
            result = oceanone_api.fetchTradePrice(self.base_asset_id, self.target_asset_id)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
        print("Ocean Thread")


class Mixin_node_info_Thread(QRunnable):
    def __init__(self, *args, **kwargs):
        super(Mixin_node_info_Thread, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            main_net_info = wallet_api.main_net_info()
            main_net_node = wallet_api.github_main_net_node_info()
            main_net_result = [main_net_info, main_net_node]

        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(main_net_result)
        finally:
            self.signals.finished.emit()
        print("Mixin_node_info_Thread")


class MixinTopAsset_Thread(QRunnable):
    def __init__(self, *args, **kwargs):
        super(MixinTopAsset_Thread, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            top_asset_list = wallet_api.top_asset_mixin_network()
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(top_asset_list)
        finally:
            self.signals.finished.emit()
        print("ExinPrice Thread")


class ExinPrice_Thread(QRunnable):
    def __init__(self, base_asset_id, target_asset_id = "", delay_seconds = 0,  *args, **kwargs):
        super(ExinPrice_Thread, self).__init__()
        self.target_asset_id = target_asset_id
        self.base_asset_id = base_asset_id
        self.delay_seconds = delay_seconds
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            time.sleep(self.delay_seconds)
            result = exincore_api.fetchExinPrice(self.base_asset_id, self.target_asset_id)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
        print("ExinPrice Thread")

class Balance_Thread(QRunnable):
    def __init__(self, wallet_obj, delay_seconds = 0,  *args, **kwargs):
        super(Balance_Thread, self).__init__()
        self.wallet_obj = wallet_obj
        self.delay_seconds = delay_seconds
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            time.sleep(self.delay_seconds)
            result = self.wallet_obj.get_balance()
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
        print("Balance Thread")
class UserProfile_Thread(QRunnable):
    def __init__(self, wallet_obj, *args, **kwargs):
        super(UserProfile_Thread, self).__init__()
        self.wallet_obj = wallet_obj
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.wallet_obj.fetch_my_profile()
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
        print("User profile Thread")


class CreateAccount_Thread(QRunnable):
    def __init__(self, user_input_name, user_input_pin, user_input_file, *args, **kwargs):
        super(CreateAccount_Thread, self).__init__()
        self.user_input_name = user_input_name
        self.user_input_pin  = user_input_pin
        self.user_input_file = user_input_file
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.signals.progress.emit("Generating key file")
            thisAccountRSAKeyPair = wallet_api.RSAKey4Mixin()
            body = {
                "session_secret": thisAccountRSAKeyPair.session_key,
                "full_name": self.user_input_name
            }
            wallet_obj = wallet_api.WalletRecord("","","", "","")
            self.signals.progress.emit("Fetching authentication token to create wallet")
            token2create = wallet_api.fetchTokenForCreateUser(body, "http://freemixinapptoken.myrual.me/token")

            self.signals.progress.emit("Creating wallet")
            create_wallet_result = wallet_obj.create_wallet(thisAccountRSAKeyPair.session_key, self.user_input_name, token2create)
            if(create_wallet_result.is_success):
                self.signals.progress.emit("Writing wallet into file")

                create_wallet_result.data.private_key = thisAccountRSAKeyPair.private_key
                new_wallet = wallet_api.WalletRecord("",create_wallet_result.data.user_id, create_wallet_result.data.session_id, create_wallet_result.data.pin_token, create_wallet_result.data.private_key)
     
                wallet_api.write_wallet_into_clear_base64_file(create_wallet_result.data, self.user_input_file)
                create_pin_result = new_wallet.update_pin("", self.user_input_pin)
                if(create_pin_result.is_success):
                    self.signals.progress.emit("Pin is created")
                else:
 
                    self.signals.progress.emit("Failed to create pin. Update pin later")
                self.signals.progress.emit("Generating deposit address")
                engine = sqlalchemy.create_engine('sqlite:///' + self.user_input_file + '.snapshot.db')
                # Create all tables in the engine. This is equivalent to "Create Table"
                # statements in raw SQL.
                mixin_sqlalchemy_type.Base.metadata.create_all(engine)
                mixin_sqlalchemy_type.Base.metadata.bind = engine
 
                DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
                self.session = DBSession()


                for eachAssetID in mixin_asset_id_collection.MIXIN_DEFAULT_CHAIN_GROUP:
                    this_balance = new_wallet.get_singleasset_balance(eachAssetID)
                    if(this_balance.is_success):
                        self.signals.progress.emit("Generated deposit address for " + this_balance.data.name)
                self.signals.result.emit(self.user_input_file)
            else:
                self.signals.progress.emit("Failed to create wallet")
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(True)
        finally:
            self.signals.finished.emit()


def asset_is_main_chain_token(asset):
    return asset.chain_id == asset.asset_id 

def foundMainChainName(chain_id, balance_result_list):
    for eachAssetPublicChain in balance_result_list:
        if asset_is_main_chain_token(eachAssetPublicChain) and eachAssetPublicChain.chain_id == chain_id:
            return eachAssetPublicChain.name
    return False
class SnapExplain_TableModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """
    def __init__(self, parent, data, header,  *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = data
        self.header = header
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return 1       
    def data(self, index, role):
        if not index.isValid():
            return None

        value = self.mylist[index.row()]
        if role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self.header[col]
        return None

class AssetIntro_TableModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """
    def __init__(self, parent, eachAsset, balance_result_list, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        thisRecord = []
        self.header = []

        thisRecord.append(eachAsset.name)
        self.header.append("Name")
        chain_name = foundMainChainName(eachAsset.chain_id, balance_result_list)
        if chain_name != False:
            thisRecord.append(chain_name)
            self.header.append("Main chain")
            if asset_is_main_chain_token(eachAsset):
                thisRecord.append("Main chain native token")
                self.header.append("token type")
            else:
                thisRecord.append("Token issued by contract")
                self.header.append("token type")
                if eachAsset.chain_id == mixin_asset_id_collection.ETH_ASSET_ID:
                    thisRecord.append("https://etherscan.io/address/" + eachAsset.asset_key)
                    self.header.append("Info on main chain")
                elif eachAsset.chain_id == mixin_asset_id_collection.EOS_ASSET_ID:
                    thisRecord.append("https://eosflare.io/token/" + eachAsset.asset_key.replace(":", "/"))
                    self.header.append("Info on main chain")
                else:
                    self.header.append("token contract on main chain")
                    thisRecord.append(chain_name + " contract : " + eachAsset.asset_key)
        else:
            thisRecord.append(eachAsset.chain_id)
            self.header.append("Chain ID")
            thisRecord.append(eachAsset.asset_key)
            self.header.append("asset key")

        thisRecord.append("https://mixin.one/snapshots/"+eachAsset.asset_id)
        self.header.append("Info on Mixin Newtork")
        self.mylist = thisRecord
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return 1       
    def data(self, index, role):
        if not index.isValid():
            return None

        value = self.mylist[index.row()]
        if role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self.header[col]
        return None



class AssetDetail_TableModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """
    def __init__(self, parent, eachAsset, balance_result_list,  *args):
        QAbstractTableModel.__init__(self, parent, *args)
        thisRecord = []
        chain_name = foundMainChainName(eachAsset.chain_id, balance_result_list)
        if chain_name != False:
            thisRecord.append(chain_name)
            if asset_is_main_chain_token(eachAsset):
                thisRecord.append("Main chain token")
            else:
                thisRecord.append(chain_name + " contract : " + eachAsset.asset_key)
        else:
            thisRecord.append("")
            thisRecord.append("")
        if eachAsset.chain_id in mixin_asset_id_collection.Block_interval:
            pending_seconds = mixin_asset_id_collection.Block_interval[eachAsset.chain_id] * eachAsset.confirmations
            if pending_seconds < 60:
                thisRecord.append(str(pending_seconds) + " seconds")
            else:
                pending_minutes = pending_seconds/60
                thisRecord.append(str(int(pending_minutes)) + " minutes")
        else:
            thisRecord.append("NA")

        if eachAsset.chain_id == mixin_asset_id_collection.EOS_ASSET_ID:
            thisRecord.append(eachAsset.account_name)
            thisRecord.append(eachAsset.account_tag)
            self.mylist = thisRecord
            self.header = ["Main chain", "Token type", "Deposit confirmation duration", "Deposit account name", "Deposit payment memo:"]
        else:
            thisRecord.append(eachAsset.public_key)
            self.mylist = thisRecord
            self.header = ["Main chain", "Token type", "Deposit confirmation duration", "Deposit address"]
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return 1       
    def data(self, index, role):
        if not index.isValid():
            return None

        value = self.mylist[index.row()]
        if role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self.header[col]
        return None


class Balance_TableModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """
    def __init__(self, parent, balance_result_list, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        finalData = []
        for eachAsset in balance_result_list:
            thisRecord = []
            thisRecord.append(eachAsset.name)
            thisRecord.append(eachAsset.balance)
            this_asset_value_in_usd_in_float =  float(eachAsset.balance) * float(eachAsset.price_usd)
            usd_value_with_twodigi_after_dot = int(100 * this_asset_value_in_usd_in_float)/100
            thisRecord.append(str(usd_value_with_twodigi_after_dot) + " usd")
            thisRecord.append(eachAsset.price_usd)
            finalData.append(thisRecord)

        self.mylist = finalData
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        if len(self.mylist) > 0:
            return len(self.mylist[0])
        return 0
        
    def data(self, index, role):
        if not index.isValid():
            return None
        value = self.mylist[index.row()][index.column()]
        if role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

class MixinAsset_TableModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """
    def __init__(self, parent, mixin_asset_record, header = ["name", "symbol", "asset-id"], *args):
        QAbstractTableModel.__init__(self, parent, *args)
        finalData = []
        for eachOrder in mixin_asset_record:
            thisRecord = []
            thisRecord.append(eachOrder.asset_name)
            thisRecord.append(eachOrder.asset_symbol)
            thisRecord.append("https://mixin.one/snapshots/"+eachOrder.asset_id)
            finalData.append(thisRecord)

        self.mylist = finalData
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        if len(self.mylist) > 0:
            return len(self.mylist[0])
        return 0
        
    def data(self, index, role):
        if not index.isValid():
            return None
        value = self.mylist[index.row()][index.column()]
        if role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None


class OceanOrder_TableModel(QAbstractTableModel):

    """
    keep the method names
    they are an integral part of the model
    """
    def __init__(self, parent, ocean_order_group, header = ["price", "amount", "funds"], *args):
        QAbstractTableModel.__init__(self, parent, *args)
        finalData = []
        for eachOrder in ocean_order_group:
            thisRecord = []
            thisRecord.append(eachOrder.price)
            thisRecord.append(eachOrder.amount)
            thisRecord.append(eachOrder.funds)
            finalData.append(thisRecord)

        self.mylist = finalData
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        if len(self.mylist) > 0:
            return len(self.mylist[0])
        return 0
        
    def data(self, index, role):
        if not index.isValid():
            return None
        value = self.mylist[index.row()][index.column()]
        if role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None


class ExinPrice_TableModel(QAbstractTableModel):

    """
    keep the method names
    they are an integral part of the model
    """
    def __init__(self, parent, exintrade_price_list, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        finalData = []
        for eachAsset in exintrade_price_list:
            thisRecord = []
            thisRecord.append(eachAsset.price)
            thisRecord.append(eachAsset.exchange_asset_symbol )
            thisRecord.append(eachAsset.minimum_amount)
            thisRecord.append(eachAsset.maximum_amount)

            finalData.append(thisRecord)

        self.mylist = finalData
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        if len(self.mylist) > 0:
            return len(self.mylist[0])
        return 0
        
    def data(self, index, role):
        if not index.isValid():
            return None
        value = self.mylist[index.row()][index.column()]
        if role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None
plugins_func_list = [exincore_api.exincore_can_explain_snapshot, oceanone_api.oceanone_can_explain_snapshot]
def Snapshot_fromSql(transaction_record_in_item):
    singleSnapShot                  = wallet_api.Snapshot()
    singleSnapShot.snapshot_id      = transaction_record_in_item.snap_snapshot_id
    singleSnapShot.type             = transaction_record_in_item.snap_type
    singleSnapShot.amount           = transaction_record_in_item.snap_amount
    singleSnapShot.created_at       = transaction_record_in_item.snap_created_at
    singleSnapShot.asset            = wallet_api.Static_Asset()

    singleSnapShot.asset.asset_id   = transaction_record_in_item.snap_asset_asset_id
    singleSnapShot.asset.chain_id   = transaction_record_in_item.snap_asset_chain_id
    singleSnapShot.asset.name       = transaction_record_in_item.snap_asset_name
    singleSnapShot.asset.symbol     = transaction_record_in_item.snap_asset_symbol
    singleSnapShot.source           = transaction_record_in_item.snap_source
    singleSnapShot.user_id          = transaction_record_in_item.snap_user_id
    singleSnapShot.opponent_id      = transaction_record_in_item.snap_opponent_id
    singleSnapShot.trace_id         = transaction_record_in_item.snap_trace_id
    singleSnapShot.memo             = transaction_record_in_item.snap_memo
    return singleSnapShot


def plugin_can_explain_snapshot(input_snapshot):
    for eachFunc in plugins_func_list:
        result = eachFunc(input_snapshot)
        if result != False:
            return result
    return False


class OceanHistoryTableModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """
    def __init__(self, parent, oceanhistory_list, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        finalData = []
        for eachSqlRecord in oceanhistory_list:
            thisRecord = []
            thisRecord.append(eachSqlRecord.pay_asset_id)
            thisRecord.append(eachSqlRecord.pay_asset_amount)
            thisRecord.append(eachSqlRecord.asset_id)
            thisRecord.append(eachSqlRecord.price)
            thisRecord.append(eachSqlRecord.operation_type)
            thisRecord.append(eachSqlRecord.side)
            thisRecord.append(eachSqlRecord.order_id)
            finalData.append(thisRecord)

        self.mylist = finalData
        self.header = header 

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        if len(self.mylist) > 0:
            return len(self.mylist[0])
        return 0
        
    def data(self, index, role):
        if not index.isValid():
            return None
        value = self.mylist[index.row()][index.column()]
        if role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

class TransactionHistoryTableModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """
    def __init__(self, parent, MySnapshot_list, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        finalData = []
        for eachSqlRecord in MySnapshot_list:
            thisRecord = []
            thisRecord.append(eachSqlRecord.snap_created_at)
            thisRecord.append(eachSqlRecord.snap_type)
            thisRecord.append(eachSqlRecord.snap_amount)
            thisRecord.append(eachSqlRecord.snap_asset_symbol)

 
            thisSnapshot = Snapshot_fromSql(eachSqlRecord)
            thisRecord.append(eachSqlRecord.snap_opponent_id)
            thisRecord.append(eachSqlRecord.snap_memo)
            finalData.append(thisRecord)

        self.mylist = finalData
        self.header = ["Created at", "Type", "Amount", "Asset", "opponent", "memo"]

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        if len(self.mylist) > 0:
            return len(self.mylist[0])
        return 0
        
    def data(self, index, role):
        if not index.isValid():
            return None
        value = self.mylist[index.row()][index.column()]
        if role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

class Fullnodes_TableModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """
    def __init__(self, parent, fullnodes_list, github_node_info, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        finalData = []
        for eachNode in fullnodes_list:
            thisRecord = []
            thisRecord.append(eachNode.state)
            thisRecord.append(eachNode.node)
            thisRecord.append(eachNode.payee)
            thisRecord.append(eachNode.signer)

            i = 0
            for eachGithub in github_node_info:
                if eachNode.signer == eachGithub.get("signer"):
                    thisRecord.append(eachGithub.get("host"))
                    break
                else:
                    i+=1
            if i == len(github_node_info):
                thisRecord.append("Anonymous")
            thisRecord.append(str(datetime.date.fromtimestamp((eachNode.timestamp)/(1000 * 1000 * 1000))))
            finalData.append(thisRecord)
        self.mylist = finalData
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        if len(self.mylist) > 0:
            return len(self.mylist[0])
        return 0
        
    def data(self, index, role):
        if not index.isValid():
            return None
        value = self.mylist[index.row()][index.column()]
        if role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None


class TopAsset_TableModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """
    def __init__(self, parent, topasset_list, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        finalData = []
        for eachAsset in topasset_list:
            thisRecord = []
            thisRecord.append(eachAsset.symbol)
            thisRecord.append("{:,}".format(int(float(eachAsset.capitalization))))
            thisRecord.append(eachAsset.price_usd)
            thisRecord.append("https://mixin.one/snapshots/"+eachAsset.asset_id)
            finalData.append(thisRecord)
        self.mylist = finalData
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        if len(self.mylist) > 0:
            return len(self.mylist[0])
        return 0
        
    def data(self, index, role):
        if not index.isValid():
            return None
        value = self.mylist[index.row()][index.column()]
        if role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        button_action = QAction("Open wallet file", self)
        button_action.setStatusTip("Open wallet file")
        button_action.triggered.connect(self.open_file)
 
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction(button_action)

        pin_menu = menu.addMenu("Pin")
        self.verify_pin_action = QAction("verify pin", self)
        self.verify_pin_action.triggered.connect(self.pop_verify_pin_window)
        pin_menu.addAction(self.verify_pin_action)
        self.update_pin_action = QAction("update pin", self)
        self.update_pin_action.triggered.connect(self.pop_update_pin_window)
        pin_menu.addAction(self.update_pin_action)

        self.counter = 0
        layout = QVBoxLayout()
        self.rootLayout = layout

        b = QPushButton("Open Wallet file")
        b.pressed.connect(self.open_file)
        layout.addWidget(b)
        new_wallet_btn = QPushButton("Create Wallet file")
        new_wallet_btn.pressed.connect(self.pop_create_wallet_window)
        layout.addWidget(new_wallet_btn)


        self.w = QWidget()
        self.w.setLayout(layout)
        self.w.show()
        self.timer = QTimer()
        self.timer.setInterval(1000)

        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

        self.threadPool = QThreadPool()
        self.threadPool.setMaxThreadCount(8)
        print("Multithreading with maximum %d threads" % self.threadPool.maxThreadCount())
    def create_transaction_history(self, all_transaction_history_list):

        header = ["Amount", "Asset", "Created at", "opponent", "Type"]
        this_tableModel = TransactionHistoryTableModel(None, all_transaction_history_list, header)

        transaction_table_view = QTableView()
        transaction_table_view.setModel(this_tableModel)
        return transaction_table_view



    def open_asset_transaction_history(self):
        self.asset_transaction_history_list = self.session.query(mixin_sqlalchemy_type.MySnapshot).filter_by(snap_asset_asset_id = self.asset_instance_in_item.asset_id).order_by(mixin_sqlalchemy_type.MySnapshot.id.desc()).all()
        self.widget_transaction_list_detail = self.create_transaction_history(self.asset_transaction_history_list)
        if len(self.asset_transaction_history_list) > 0:
            header = self.widget_transaction_list_detail.horizontalHeader()       
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

        self.widget_transaction_list_detail.clicked.connect(self.asset_transaction_record_selected)
        self.widget_transaction_list_detail.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.asset_transaction_explain_label = QLabel("")
        asset_transaction_layout = QVBoxLayout()
        asset_transaction_layout.addWidget(QLabel("History of " + self.asset_instance_in_item.name))
        asset_transaction_layout.addWidget(self.asset_transaction_explain_label)
        asset_transaction_layout.addWidget(self.widget_transaction_list_detail)
        self.asset_transaction_widget = QWidget()
        self.asset_transaction_widget.setLayout(asset_transaction_layout)
        self.asset_transaction_widget.show()



    def update_transaction_history(self):
        self.all_transaction_history_list = self.session.query(mixin_sqlalchemy_type.MySnapshot).order_by(mixin_sqlalchemy_type.MySnapshot.id.desc()).all()
        header = ["Amount", "Asset", "Created at", "opponent", "Type"]
        this_tableModel = TransactionHistoryTableModel(None, self.all_transaction_history_list, header)
        self.account_transaction_history_widget.setModel(this_tableModel)
        self.account_transaction_history_widget.update()
        if len(self.all_transaction_history_list) > 0:
            header = self.account_transaction_history_widget.horizontalHeader()       
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)






    def open_transaction_history(self):
        self.all_transaction_history_list = self.session.query(mixin_sqlalchemy_type.MySnapshot).order_by(mixin_sqlalchemy_type.MySnapshot.id.desc()).all()
        return self.create_transaction_history(self.all_transaction_history_list)

    def execute_this_fn(self):
        for i in range(0, 5):
            time.sleep(1)
        return "Done."
    def print_output(self, s):
        print(s)
    def snap_thread_complete(self):
        print("snap_thread_complete, total %d active thread"%self.threadPool.activeThreadCount())

    def snap_thread_error_complete(self):
        print("snap_thread_error_complete, total %d active thread"%self.threadPool.activeThreadCount())
        self.mysnapshots_worker = AccountsSnapshots_Thread(self.selected_wallet_record, self.the_last_snapshots_time, 10)
        self.mysnapshots_worker.signals.result.connect(self.received_snapshot)
        self.mysnapshots_worker.signals.finished.connect(self.snap_thread_complete)
        self.mysnapshots_worker.signals.error.connect(self.snap_thread_error_complete)
        self.threadPool.start(self.mysnapshots_worker)

    def thread_complete(self):
        print("THREAD COMPLETE")
    def exin_thread_complete(self):
        print("EXIN THREAD COMPLETE")
        if self.account_tab_widget.currentIndex() == 1:
            exin_worker = ExinPrice_Thread(mixin_asset_id_collection.USDT_ASSET_ID, "", 60)
            exin_worker.signals.result.connect(self.received_exin_result)
            exin_worker.signals.finished.connect(self.exin_thread_complete)
            self.threadPool.start(exin_worker)
        else:
            return

    def balance_load_thread_complete(self):
        print("Balance THREAD COMPLETE")
        if self.account_tab_widget.currentIndex() == 0:
            worker = Balance_Thread(self.selected_wallet_record, 60)
            worker.signals.result.connect(self.received_balance_result)
            worker.signals.finished.connect(self.balance_load_thread_complete)
            self.threadPool.start(worker)
        else:
            return

    def create_wallet_confirm_chosen_block(self,user_input_name, user_input_pin, user_input_file):

        thisAccountRSAKeyPair = wallet_api.RSAKey4Mixin()
        body = {
            "session_secret": thisAccountRSAKeyPair.session_key,
            "full_name": user_input_name
        }
        wallet_obj = wallet_api.WalletRecord("","","", "","")
        self.create_account_layout.addWidget(QLabel("Created key file"))
 
        token2create = wallet_api.fetchTokenForCreateUser(body, "http://freemixinapptoken.myrual.me/token")
 
        create_wallet_result = wallet_obj.create_wallet(thisAccountRSAKeyPair.session_key, user_input_name, token2create)
        if(create_wallet_result.is_success):
            self.create_account_layout.addWidget(QLabel("Created account"))

            create_wallet_result.data.private_key = thisAccountRSAKeyPair.private_key
            new_wallet = wallet_api.WalletRecord("",create_wallet_result.data.user_id, create_wallet_result.data.session_id, create_wallet_result.data.pin_token, create_wallet_result.data.private_key)
 
            wallet_api.write_wallet_into_clear_base64_file(create_wallet_result.data, user_input_file)
            self.create_account_layout.addWidget(QLabel("Wrote account info into "+user_input_file))

            create_pin_result = new_wallet.update_pin("", user_input_pin)
            for eachAssetID in mixin_asset_id_collection.MIXIN_DEFAULT_CHAIN_GROUP:
                print(eachAssetID)
                asset_result = new_wallet.get_singleasset_balance(eachAssetID)
                if(asset_result.is_success):
                    self.create_account_layout.addWidget(QLabel("Created deposit address for " + asset_result.data.name))
            if(create_pin_result.is_success):
                self.create_account_layout.addWidget(QLabel("Created pin"))

            else:
                self.create_account_layout.addWidget(QLabel("Failed to create pin"))
        else:
             self.create_account_layout.addWidget(QLabel("Failed to create account"))
           

    def open_verify_pin_window(self):
        print("verify pin")
    def open_update_pin_window(self):
        print("update pin")
    def open_file(self):
        file_name_selected = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "","mixinkey Files (*.mixinkey);;All Files (*)")
        file_name = file_name_selected[0]
        fileter   = file_name_selected[1]
        if(file_name == ''):
            print("User cancel file")
        else:
            print("User select file with %s" % file_name)
            self.file_name = file_name
            self.selected_wallet_record = wallet_api.load_wallet_from_clear_base64_file(file_name)
            self.open_selected_wallet()
            self.w.close()
    def select_file_for_create_wallet(self):
        file_name_selected = QFileDialog.getSaveFileName(self, "QFileDialog.getOpenFileName()", "","mixinkey Files (*.mixinkey);;All Files (*)")
        file_name = file_name_selected[0]
        fileter   = file_name_selected[1]
        if(file_name == ''):
            print("User cancel file")
        else:
            print("User select file with %s" % file_name)
            self.file_selected_edit.setText(file_name)

    def create_wallet_progress_update(self, obj):
        print(obj)
        self.create_account_layout.addWidget(QLabel(obj))
    def create_account_button_pressed(self):
        self.create_account_widget.close()
        self.file_name = self.user_input_file
        self.selected_wallet_record = wallet_api.load_wallet_from_clear_base64_file(self.user_input_file)
        self.open_selected_wallet()
        self.user_input_file = None
        self.w.close()

    def create_account_finished_callback(self):
        Successful_created_account_button = QPushButton("Open wallet")
        Successful_created_account_button.pressed.connect(self.create_account_button_pressed)
        self.create_account_layout.addWidget(Successful_created_account_button)

    def create_account_pressed(self):
        user_input_pin  = self.pin_selected_edit.text()
        self.user_input_file = self.file_selected_edit.text()
        #self.create_wallet_confirm_chosen_block(wallet_api.randomString(), user_input_pin, user_input_file)

        worker = CreateAccount_Thread(wallet_api.randomString(), user_input_pin, self.user_input_file)
        worker.signals.progress.connect(self.create_wallet_progress_update)
        worker.signals.finished.connect(self.create_account_finished_callback)
        self.threadPool.start(worker)
        self.go_create_accout_btn.setDisabled(True)
        

    def close_Create_Windows(self):
        self.create_withdraw_address_widget.close()
        worker = Asset_addresses_Thread(self.selected_wallet_record, self.asset_instance_in_item)
        worker.signals.result.connect(self.received_asset_withdraw_addresses_result)
        worker.signals.finished.connect(self.thread_complete)
        self.threadPool.start(worker)
    def close_Create_Mainnet_Windows(self):
        self.create_withdraw_address_widget.close()
        if True:
            for i in self.mainnet_address_list:
                self.mainnet_withdraw_addresses_list_widget.takeItem(0)
            self.mainnet_address_list = []

            Main_net_address_list = self.session.query(mixin_sqlalchemy_type.Main_net_address).all()
            for each_mainnet_address in Main_net_address_list:
                this_list_item = QListWidgetItem()
                this_list_item.setData(0x0100, each_mainnet_address)
                this_list_item.setText(each_mainnet_address.name)
                self.mainnet_withdraw_addresses_list_widget.addItem(this_list_item)
                self.mainnet_address_list.append(this_list_item)
            self.mainnet_withdraw_addresses_list_widget.update()
        return


    def pressed_create_mainnet_withdraw_address(self):
        print("Account tag %s, deposit address %s"%(self.account_tag_edit.text(), self.public_key_edit.text()))
        new_main_net_address = mixin_sqlalchemy_type.Main_net_address()
        new_main_net_address.name = self.account_tag_edit.text()
        new_main_net_address.address = self.public_key_edit.text()
        self.session.add(new_main_net_address)
        self.session.commit()

        OK_button = QPushButton("Done")
        OK_button.pressed.connect(self.close_Create_Mainnet_Windows)
        self.create_withdraw_address_layout.addWidget(OK_button)

    def pressed_create_withdraw_address_bitcoin(self):
        print("Account tag %s, deposit address %s, pin %s"%(self.account_tag_edit.text(), self.public_key_edit.text(), self.asset_pin_edit.text()))
        self.Add_address_btn.setDisabled(True)
        create_address_result  = self.selected_wallet_record.create_address(self.asset_instance_in_item.asset_id, self.public_key_edit.text(), self.account_tag_edit.text(), asset_pin = self.asset_pin_edit.text())
        if create_address_result.is_success:
            print("Address is created with id %s"%create_address_result.data.address_id)
            OK_button = QPushButton("Done")
            OK_button.pressed.connect(self.close_Create_Windows)
            self.create_withdraw_address_layout.addWidget(OK_button)
        else:
            print("Failed to create address because "%str(create_address_result))
            failed_msg = QMessageBox()
            failed_msg.setText("Failed to create address %s"%str(create_address_result))
            failed_msg.exec_()
    def pressed_create_withdraw_address_eos(self):
        print("Account name %s, account memo %s, pin %s"%(self.account_name_edit.text(), self.account_memo_edit.text(), self.asset_pin_edit.text()))
        self.Add_address_btn.setDisabled(True)
        create_address_result  = self.selected_wallet_record.create_address(self.asset_instance_in_item.asset_id, "", "", self.asset_pin_edit.text(), self.account_name_edit.text(), self.account_memo_edit.text())
        if create_address_result.is_success:
            print("Address is created with id %s"%create_address_result.data.address_id)
            OK_button = QPushButton("Done")
            OK_button.pressed.connect(self.close_Create_Windows)
            self.create_withdraw_address_eos_layout.addWidget(OK_button)
        else:
            print("Failed to create address because "%str(create_address_result))
            failed_msg = QMessageBox()
            failed_msg.setText("Failed to create address %s"%str(create_address_result))
            failed_msg.exec_()


    def pressed_remove_withdraw_address_bitcoin(self):
        self.Remove_address_btn.setDisabled(True)
        remove_address_result  = self.selected_wallet_record.remove_address(self.withdraw_address_instance_in_item.address_id, self.asset_pin_edit.text())
        if remove_address_result.is_success:
            self.remove_withdraw_address__widget.close()
            worker = Asset_addresses_Thread(self.selected_wallet_record, self.asset_instance_in_item)
            worker.signals.result.connect(self.received_asset_withdraw_addresses_result)
            worker.signals.finished.connect(self.thread_complete)
            self.threadPool.start(worker)

        else:
            print("Failed to remove address %s"%str(remove_address_result))

            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Failed to create address %s"%str(remove_address_result))
            congratulations_msg.exec_()

    def pressed_verify_pin(self):
        verify_pin_result  = self.selected_wallet_record.verify_pin(self.asset_pin_edit.text())
        if(verify_pin_result.is_success):
            self.verify_pin_widget.close()
            load_wallet_msg = QMessageBox()
            load_wallet_msg.setText("Pin is correct")
            load_wallet_msg.exec_()
        else:
            load_wallet_msg = QMessageBox()
            print(verify_pin_result.error.status)
            if verify_pin_result.error.status == 202 and verify_pin_result.error.code == 20119:
                print("pin incorrect")
                load_wallet_msg.setText(str(verify_pin_result.error.description))
            else:
                print("other error")
                load_wallet_msg.setText(str(verify_pin_result))
            load_wallet_msg.exec_()

    def pressed_update_pin(self):
        update_pin_result  = self.selected_wallet_record.update_pin(self.asset_pin_edit.text(), self.update_new_pin_edit.text())
        if(update_pin_result.is_success):
            print("success")
            self.update_pin_widget.close()
            load_wallet_msg = QMessageBox()
            load_wallet_msg.setText("Successfully updated pin")
            load_wallet_msg.exec_()
        else:
            load_wallet_msg = QMessageBox()
            load_wallet_msg.setText(str(update_pin_result))
            load_wallet_msg.exec_()


    def pop_verify_pin_window(self):


        if (not hasattr(self, "selected_wallet_record")):
            load_wallet_msg = QMessageBox()
            load_wallet_msg.setText("Please load wallet file")
            load_wallet_msg.exec_()
            return

        asset_pin_widget     = QLabel("Pin:")
        self.asset_pin_edit  = QLineEdit()
        self.asset_pin_edit.setEchoMode(QLineEdit.Password)
        self.asset_pin_edit.setMaxLength(6)
        Remove_address_btn       = QPushButton("Verify")
        Remove_address_btn.pressed.connect(self.pressed_verify_pin)
        self.Remove_address_btn = Remove_address_btn

        verify_pin_layout = QVBoxLayout()
        verify_pin_layout.addWidget(asset_pin_widget)
        verify_pin_layout.addWidget(self.asset_pin_edit)
        verify_pin_layout.addWidget(Remove_address_btn)

        self.verify_pin_widget = QWidget()
        self.verify_pin_widget.setLayout(verify_pin_layout)
        self.verify_pin_widget.show()

    def pop_update_pin_window(self):


        if (not hasattr(self, "selected_wallet_record")):
            load_wallet_msg = QMessageBox()
            load_wallet_msg.setText("Please load wallet file")
            load_wallet_msg.exec_()
            return

        asset_pin_widget     = QLabel("Old pin:")
        self.asset_pin_edit  = QLineEdit()
        self.asset_pin_edit.setEchoMode(QLineEdit.Password)
        self.asset_pin_edit.setMaxLength(6)
        asset_new_pin_widget     = QLabel("New pin:")
        self.update_new_pin_edit  = QLineEdit()
        self.update_new_pin_edit.setEchoMode(QLineEdit.Password)
        self.update_new_pin_edit.setMaxLength(6)

        update_pin_btn       = QPushButton("Update")
        update_pin_btn.pressed.connect(self.pressed_update_pin)

        update_pin_layout = QVBoxLayout()
        update_pin_layout.addWidget(asset_pin_widget)
        update_pin_layout.addWidget(self.asset_pin_edit)
        update_pin_layout.addWidget(asset_new_pin_widget)
        update_pin_layout.addWidget(self.update_new_pin_edit)
        update_pin_layout.addWidget(update_pin_btn)

        self.update_pin_widget = QWidget()
        self.update_pin_widget.setLayout(update_pin_layout)
        self.update_pin_widget.show()



    def pop_Remove_withdraw_address_window_bitcoinstyle(self):


        asset_pin_widget     = QLabel("Asset pin:")
        self.asset_pin_edit  = QLineEdit()
        self.asset_pin_edit.setEchoMode(QLineEdit.Password)
        self.asset_pin_edit.setMaxLength(6)
        Remove_address_btn       = QPushButton("Remove")
        Remove_address_btn.pressed.connect(self.pressed_remove_withdraw_address_bitcoin)
        self.Remove_address_btn = Remove_address_btn

        remove_withdraw_address_layout = QVBoxLayout()
        remove_withdraw_address_layout.addWidget(asset_pin_widget)
        remove_withdraw_address_layout.addWidget(self.asset_pin_edit)
        remove_withdraw_address_layout.addWidget(Remove_address_btn)

        self.remove_withdraw_address__widget = QWidget()
        self.remove_withdraw_address__widget.setLayout(remove_withdraw_address_layout)
        self.remove_withdraw_address__widget.show()
    def pop_Remove_mainnet_withdraw_address_window_bitcoinstyle(self):
        self.session.delete(self.mainnet_address_instance_in_item)
        for i in self.mainnet_address_list:
            self.mainnet_withdraw_addresses_list_widget.takeItem(0)
        self.mainnet_address_list = []

        Main_net_address_list = self.session.query(mixin_sqlalchemy_type.Main_net_address).all()
        for each_mainnet_address in Main_net_address_list:
            this_list_item = QListWidgetItem()
            this_list_item.setData(0x0100, each_mainnet_address)
            this_list_item.setText(each_mainnet_address.name)
            self.mainnet_withdraw_addresses_list_widget.addItem(this_list_item)
            self.mainnet_address_list.append(this_list_item)
        self.mainnet_withdraw_addresses_list_widget.update()

    def pop_create_withdraw_address_window_eosstyle(self):


        account_name_widget    = QLabel("Account name:")
        self.account_name_edit = QLineEdit()
        account_memo_widget      = QLabel("Account memo:")
        self.account_memo_edit = QLineEdit()
        asset_pin_widget       = QLabel("Asset pin:")
        self.asset_pin_edit    = QLineEdit()
        self.asset_pin_edit.setEchoMode(QLineEdit.Password)
        self.asset_pin_edit.setMaxLength(6)
        Add_address_btn       = QPushButton("Create")
        Add_address_btn.pressed.connect(self.pressed_create_withdraw_address_eos)
        self.Add_address_btn = Add_address_btn

        create_withdraw_address_layout = QVBoxLayout()
        create_withdraw_address_layout.addWidget(account_name_widget)
        create_withdraw_address_layout.addWidget(self.account_name_edit)
        create_withdraw_address_layout.addWidget(account_memo_widget)
        create_withdraw_address_layout.addWidget(self.account_memo_edit)
        create_withdraw_address_layout.addWidget(asset_pin_widget)
        create_withdraw_address_layout.addWidget(self.asset_pin_edit)
        create_withdraw_address_layout.addWidget(Add_address_btn)

        self.create_withdraw_address_eos_layout = create_withdraw_address_layout

        self.create_withdraw_address_widget = QWidget()
        self.create_withdraw_address_widget.setLayout(create_withdraw_address_layout)
        self.create_withdraw_address_widget.show()


    def pop_create_mainnet_address_window_bitcoinstyle(self):


        account_tag_widget    = QLabel("Account alias:")
        self.account_tag_edit = QLineEdit()
        public_key_widget     = QLabel("Mixin main net address:")
        self.public_key_edit  = QLineEdit()
        Add_mainnet_address_btn       = QPushButton("Create")
        Add_mainnet_address_btn.pressed.connect(self.pressed_create_mainnet_withdraw_address)

        create_withdraw_address_layout = QVBoxLayout()
        create_withdraw_address_layout.addWidget(account_tag_widget)
        create_withdraw_address_layout.addWidget(self.account_tag_edit)
        create_withdraw_address_layout.addWidget(public_key_widget)
        create_withdraw_address_layout.addWidget(self.public_key_edit)
        create_withdraw_address_layout.addWidget(Add_mainnet_address_btn)

        self.create_withdraw_address_layout = create_withdraw_address_layout

        self.create_withdraw_address_widget = QWidget()
        self.create_withdraw_address_widget.setLayout(create_withdraw_address_layout)
        self.create_withdraw_address_widget.show()


    def pop_create_withdraw_address_window_bitcoinstyle(self):


        account_tag_widget    = QLabel("Account alias:")
        self.account_tag_edit = QLineEdit()
        public_key_widget     = QLabel("Deposit address:")
        self.public_key_edit  = QLineEdit()
        asset_pin_widget     = QLabel("Asset pin:")
        self.asset_pin_edit  = QLineEdit()
        self.asset_pin_edit.setEchoMode(QLineEdit.Password)
        self.asset_pin_edit.setMaxLength(6)
        Add_address_btn       = QPushButton("Create")
        Add_address_btn.pressed.connect(self.pressed_create_withdraw_address_bitcoin)
        self.Add_address_btn = Add_address_btn

        create_withdraw_address_layout = QVBoxLayout()
        create_withdraw_address_layout.addWidget(account_tag_widget)
        create_withdraw_address_layout.addWidget(self.account_tag_edit)
        create_withdraw_address_layout.addWidget(public_key_widget)
        create_withdraw_address_layout.addWidget(self.public_key_edit)
        create_withdraw_address_layout.addWidget(asset_pin_widget)
        create_withdraw_address_layout.addWidget(self.asset_pin_edit)
        create_withdraw_address_layout.addWidget(Add_address_btn)

        self.create_withdraw_address_layout = create_withdraw_address_layout

        self.create_withdraw_address_widget = QWidget()
        self.create_withdraw_address_widget.setLayout(create_withdraw_address_layout)
        self.create_withdraw_address_widget.show()


    def pop_create_wallet_window(self):

        file_selection_layout = QHBoxLayout()
        file_title_widget = QLabel("Wallet file name:")
        self.file_selected_edit     = QLineEdit()
        file_browser_btn  = QPushButton("Select wallet file name")
        file_browser_btn.pressed.connect(self.select_file_for_create_wallet)
        file_selection_layout.addWidget(file_title_widget)
        file_selection_layout.addWidget(self.file_selected_edit)
        file_selection_layout.addWidget(file_browser_btn)
        file_title_selection_widget = QWidget()
        file_title_selection_widget.setLayout(file_selection_layout)

        pin_selection_layout = QHBoxLayout()
        pin_title_widget = QLabel("Asset pin(6 numbers):")
        self.pin_selected_edit     = QLineEdit()
        self.pin_selected_edit.setText("")
        self.pin_selected_edit.setMaxLength(6)
        self.pin_selected_edit.setEchoMode(QLineEdit.Password)
        pin_selection_layout.addWidget(pin_title_widget)
        pin_selection_layout.addWidget(self.pin_selected_edit)
        pin_edit_widget = QWidget()
        pin_edit_widget.setLayout(pin_selection_layout)

        self.create_account_progress_widget = QLabel("Progress")
        self.create_account_progress_widget.setAlignment(Qt.AlignCenter)

        go_create_accout_btn  = QPushButton("Create wallet")
        go_create_accout_btn.pressed.connect(self.create_account_pressed)
        self.go_create_accout_btn = go_create_accout_btn

        create_account_layout = QVBoxLayout()
        create_account_layout.addWidget(file_title_selection_widget)
        create_account_layout.addWidget(pin_edit_widget)
        create_account_layout.addWidget(go_create_accout_btn)
        create_account_layout.addWidget(self.create_account_progress_widget)

        self.create_account_layout = create_account_layout



        self.create_account_widget = QWidget()
        self.create_account_widget.setLayout(create_account_layout)
        self.create_account_widget.show()

    def create_wallet_file(self):
        file_name_selected = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "","mixinkey Files (*.mixinkey);;All Files (*)")
        file_name = file_name_selected[0]
        fileter   = file_name_selected[1]
        if(file_name == ''):
            print("User cancel file")
        else:
            print("User select file with %s" % file_name)
            self.selected_wallet_record = wallet_api.load_wallet_from_clear_base64_file(file_name)
            self.open_selected_wallet()


    def oh_no(self):
        worker = Balance_Thread(self.execute_this_fn)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        self.threadPool.start(worker)
    def recurring_timer(self):
        self.counter += 1
    def received_send_withdraw_addresses_result(self, withdraw_addresses_asset_result):
        if(withdraw_addresses_asset_result.is_success):
            self.withdraw_address_of_asset_list = withdraw_addresses_asset_result.data
            i = 0
            for eachAsset in self.withdraw_address_of_asset_list:
                if(self.asset_instance_in_item.chain_id != mixin_asset_id_collection.EOS_ASSET_ID):
                    self.send_address_selection_widget.insertItem(i, eachAsset.label, userData = eachAsset)
                else:
                    self.send_address_selection_widget.insertItem(i, eachAsset.account_tag, userData = eachAsset)
                i += 1
        return


    def received_asset_withdraw_addresses_result(self, withdraw_addresses_asset_result):
        if(withdraw_addresses_asset_result.is_success):
            for i in self.withdraw_address_list:
                self.withdraw_addresses_list_widget.takeItem(0)
            self.withdraw_address_list = []

            for eachAsset in withdraw_addresses_asset_result.data:
                this_list_item = QListWidgetItem()
                this_list_item.setData(0x0100, eachAsset)
                this_list_item.setText(eachAsset.label)
                self.withdraw_addresses_list_widget.addItem(this_list_item)
                self.withdraw_address_list.append(this_list_item)

            if(len(withdraw_addresses_asset_result.data) > 0):
                self.withdraw_addresses_list_widget.setCurrentRow(0)
            else:
                self.remove_address_btn.setDisabled(True)

            self.withdraw_addresses_list_widget.update()
        return

    def add_asset_into_localdb_if_never_see(self, asset_data):
        asset_symbol = self.fetch_asset_symbol_from_asset_id(asset_data.asset_id)
        if asset_symbol == None:
            this_asset_cache                    = mixin_sqlalchemy_type.Mixin_asset_record()
            this_asset_cache.asset_id           = asset_data.asset_id
            this_asset_cache.asset_name         = asset_data.name
            this_asset_cache.asset_symbol       = asset_data.symbol
            self.session.add(this_asset_cache)
            self.session.commit()

    def received_snapshot(self, searched_snapshots_result):
        print("received_snapshot")
        self.the_last_snapshots_time = searched_snapshots_result.data[-1].created_at
        print(self.the_last_snapshots_time)
        self.transaction_statusBar.showMessage(wallet_api.snapshot_time_difference_now(searched_snapshots_result.data[-1]))
        for eachsnapshots in searched_snapshots_result.data:
            asset_symbol = self.fetch_asset_symbol_from_asset_id(eachsnapshots.asset.asset_id)
            self.add_asset_into_localdb_if_never_see(eachsnapshots.asset)
            if (eachsnapshots.is_my_snap()):
                found_snapshot_quantity = len(self.session.query(mixin_sqlalchemy_type.MySnapshot).filter_by(snap_snapshot_id = eachsnapshots.snapshot_id).all())
                if(found_snapshot_quantity == 0):
                    my_snapshot = mixin_sqlalchemy_type.MySnapshot()
                    my_snapshot.snap_amount         = eachsnapshots.amount
                    my_snapshot.snap_type           = eachsnapshots.type
                    my_snapshot.snap_created_at     = eachsnapshots.created_at
                    my_snapshot.snap_asset_name     = eachsnapshots.asset.name
                    my_snapshot.snap_asset_asset_id = eachsnapshots.asset.asset_id
                    my_snapshot.snap_asset_chain_id = eachsnapshots.asset.chain_id
                    my_snapshot.snap_asset_symbol   = eachsnapshots.asset.symbol
                    my_snapshot.snap_snapshot_id    = eachsnapshots.snapshot_id
 
                    my_snapshot.snap_memo           = eachsnapshots.memo
                    my_snapshot.snap_source         = eachsnapshots.source
                    my_snapshot.snap_user_id        = eachsnapshots.user_id
                    my_snapshot.snap_trace_id       = eachsnapshots.trace_id
                    my_snapshot.snap_opponent_id    = eachsnapshots.opponent_id
                    self.session.add(my_snapshot)

        if len(searched_snapshots_result.data) > 0:
            last_record_in_database = self.session.query(mixin_sqlalchemy_type.ScannedSnapshots).order_by(mixin_sqlalchemy_type.ScannedSnapshots.id.desc()).first()
            the_last_snapshot = searched_snapshots_result.data[-1]
            if last_record_in_database != None:
                last_record_in_database.snap_amount         = the_last_snapshot.amount
                last_record_in_database.snap_type           = the_last_snapshot.type
                last_record_in_database.snap_created_at     = the_last_snapshot.created_at
                last_record_in_database.snap_asset_name     = the_last_snapshot.asset.name
                last_record_in_database.snap_asset_asset_id = the_last_snapshot.asset.asset_id
                last_record_in_database.snap_asset_chain_id = the_last_snapshot.asset.chain_id
                last_record_in_database.snap_asset_symbol   = the_last_snapshot.asset.symbol
                last_record_in_database.snap_snapshot_id    = the_last_snapshot.snapshot_id
            else:
                the_last_record = mixin_sqlalchemy_type.ScannedSnapshots()
                the_last_record.snap_amount         = the_last_snapshot.amount
                the_last_record.snap_type           = the_last_snapshot.type
                the_last_record.snap_created_at     = the_last_snapshot.created_at
                the_last_record.snap_asset_name     = the_last_snapshot.asset.name
                the_last_record.snap_asset_asset_id = the_last_snapshot.asset.asset_id
                the_last_record.snap_asset_chain_id = the_last_snapshot.asset.chain_id
                the_last_record.snap_asset_symbol   = the_last_snapshot.asset.symbol
                the_last_record.snap_snapshot_id    = the_last_snapshot.snapshot_id
                self.session.add(the_last_record)
            self.session.commit()


        delay_seconds = 0
        if len(searched_snapshots_result.data) < 100:
            delay_seconds = 90 
        self.mysnapshots_worker = AccountsSnapshots_Thread(self.selected_wallet_record, self.the_last_snapshots_time, delay_seconds)
        self.mysnapshots_worker.signals.result.connect(self.received_snapshot)
        self.mysnapshots_worker.signals.finished.connect(self.snap_thread_complete)
        self.mysnapshots_worker.signals.error.connect(self.snap_thread_error_complete)
        self.threadPool.start(self.mysnapshots_worker)


    def received_user_profile_result(self, user_profile_result):
        self.loggedin_user_profile = user_profile_result
        print("user is created at %s"%self.loggedin_user_profile.data.created_at)
        lastRecord = self.session.query(mixin_sqlalchemy_type.ScannedSnapshots).order_by(mixin_sqlalchemy_type.ScannedSnapshots.id.desc()).first()
        print(lastRecord)
        created_at_string = ""
        if lastRecord != None: 
            created_at_string = lastRecord.snap_created_at
        else:
            created_at_string = self.loggedin_user_profile.data.created_at
        self.mysnapshots_worker = AccountsSnapshots_Thread(self.selected_wallet_record, created_at_string)
        self.mysnapshots_worker.signals.result.connect(self.received_snapshot)
        self.mysnapshots_worker.signals.finished.connect(self.snap_thread_complete)
        self.mysnapshots_worker.signals.error.connect(self.snap_thread_error_complete)
        self.threadPool.start(self.mysnapshots_worker)
 
    def received_mixin_node_info_result(self, mixin_node_info_result):
        main_net_info = mixin_node_info_result[0]
        main_net_node = mixin_node_info_result[1]
        self.total_node_label.setText("Uptime: %s\nVersion: %s\n Total %d full nodes"%(main_net_info.uptime, main_net_info.version, len(main_net_info.graph.consensus)))
        self.mixin_network_fullnodes_table.setModel(Fullnodes_TableModel(None, main_net_info.graph.consensus, main_net_node, ["State", "Node id", "Payee", "Signer", "host", "joined time"]))

    def received_mixin_top_result(self, top_asset_list):
        self.total_value_exclude_xin_token = 0
        for each in top_asset_list:
            print("%s %s"%(each.symbol, each.capitalization))
            if each.asset_id == mixin_asset_id_collection.XIN_ASSET_ID:
                self.xin_token_price = each.price_usd
            else:
                self.total_value_exclude_xin_token += float(each.capitalization)
        self.mixin_network_topasset_table.setModel(TopAsset_TableModel(None, top_asset_list, ["Symbol", "Total value in USD", "Price", "Asset link in browser"]))
        self.total_asset_usd_value_exclude_xin_label.setText("{:,}".format(int(self.total_value_exclude_xin_token)) + " USD asset(exclude XIN token) in Mixin Network")

    def received_exin_result(self, exin_result):
        self.exin_result = exin_result
        this_model = ExinPrice_TableModel(self, exin_result, ["price in USDT", "Asset", "Min amount", "Max amount"])
        self.exin_tradelist_widget.setModel(this_model)
        self.exin_tradelist_widget.update()
        if hasattr(self, "exin_price_selected_row"):
            self.exin_tradelist_widget.selectRow(self.exin_price_selected_row)
        return

    def received_balance_result(self, balance_result):
        if(balance_result.is_success):
            final_balance_result = balance_result.data
            asset_id_from_server = []
            for eachAsset in balance_result.data:
                asset_id_from_server.append(eachAsset.asset_id)
                self.add_asset_into_localdb_if_never_see(eachAsset)

            for default_id in mixin_asset_id_collection.MIXIN_DEFAULT_CHAIN_GROUP:
                if not (default_id in asset_id_from_server):
                    asset_balance_result = self.selected_wallet_record.get_singleasset_balance(default_id)
                    if asset_balance_result.is_success:
                        final_balance_result.append(asset_balance_result.data)
            this_balance_model = Balance_TableModel(self, final_balance_result, ["Asset name", "Amount", "Market value", "Price"])
            self.balance_list_tableview.setModel(this_balance_model)
            self.balance_list_tableview.update()
            if hasattr(self, "balance_selected_row"):
                self.balance_list_tableview.selectRow(self.balance_selected_row)
            self.account_balance = balance_result.data
        return
    def withdraw_address_list_record_selection_actived(self,itemCurr, itemPre):
        if itemCurr == None:
            self.withdraw_address_of_asset_detail_label.setText("")
            return
        self.withdraw_address_instance_in_item = itemCurr.data(0x0100)
        self.update_asset_address_detail(self.withdraw_address_instance_in_item, self.withdraw_address_of_asset_detail_label)
        self.remove_address_btn.setDisabled(False)

    def update_exin_detail(self):
        self.selected_trade_buy_btn.setText("Buy " + self.selected_exin_result.exchange_asset_symbol)
        self.selected_trade_buy_btn.setDisabled(False)
        self.selected_trade_sell_btn.setText("Sell " + self.selected_exin_result.exchange_asset_symbol)
        self.selected_trade_sell_btn.setDisabled(False)

    def exin_trade_list_record_selected(self, index):
        self.exin_price_selected_row = index.row()
        self.selected_exin_result = self.exin_result[self.exin_price_selected_row]
        self.update_exin_detail()
    def update_cancel_order_btn_title(self):
        this_trade         = self.ocean_history_list[self.ocean_history_selected_row]
        self.ocean_cancel_order_btn.setText("Pay 0.00000001 %s to Cancel"%(self.asset_to_cancel_ocean_order.symbol))
        if this_trade.operation_type == "L":
            operation_string   = "Limit price "
        elif this_trade.operation_type == "M":
            operation_string = "market price "
        else:
            operation_string = "Cancel"
        if this_trade.side == "B":
            side_string = "buy"
        elif this_trade.side == "A":
            side_string = "sell"
        else:
            side_string = "None"
        asset_symbol = self.fetch_asset_symbol_from_asset_id(this_trade.asset_id)
        if asset_symbol != None:
            asset_string = asset_symbol
        else:
            asset_string = this_trade.asset_id
        self.ocean_cancel_order_label.setText("%s order %s\nprice %s\n%s %s"%(operation_string, this_trade.order_id, this_trade.price, side_string, asset_string))

    def update_reg_key_order_btn_title(self):
        self.ocean_reg_key_btn.setText("Pay 0.00000001 %s to register key"%(self.asset_to_reg_key.symbol))


    def asset_transaction_record_selected(self, index):
        transaction_history_selected_row = index.row()
        this_transaction         = self.asset_transaction_history_list[transaction_history_selected_row]
        thisSnapshot = Snapshot_fromSql(this_transaction)
        result = plugin_can_explain_snapshot(thisSnapshot)
        if result != False:
            if float(thisSnapshot.amount) > 0:
                direction = "from "
            else:
                direction = "to "
            self.asset_transaction_explain_label.setText("%s %s"%(direction, result))
        else:
            self.asset_transaction_explain_label.setText("")


    def transaction_record_selected(self, index):
        transaction_history_selected_row = index.row()
        this_transaction         = self.all_transaction_history_list[transaction_history_selected_row]
        thisSnapshot = Snapshot_fromSql(this_transaction)
        result = plugin_can_explain_snapshot(thisSnapshot)
        if result != False:
            explain_array = result.explain()
            self.transaction_record_explain_table.setModel(SnapExplain_TableModel(None, explain_array[1], explain_array[0]))
            self.transaction_record_explain_table.update()
            header = self.transaction_record_explain_table.verticalHeader()       
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)

            header = self.transaction_record_explain_table.horizontalHeader()       
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        else:
            self.transaction_record_explain_table.setModel(SnapExplain_TableModel(None, ["https://mixin.one/snapshots/" + thisSnapshot.snapshot_id], ["snapshotid"]))
            self.transaction_record_explain_table.update()


    def ocean_list_record_selected(self, index):
        self.ocean_history_selected_row = index.row()
        self.update_cancel_order_btn_title()
    def ocean_cancel_order_asset_changed(self, indexActived):
        self.asset_to_cancel_ocean_order = self.non_zero_asset_list[indexActived]
        self.update_cancel_order_btn_title()
    def ocean_reg_key_asset_changed(self, indexActived):
        self.asset_to_reg_key = self.non_zero_asset_list[indexActived]
        self.update_reg_key_order_btn_title()

    def balance_list_record_selected(self, index):
        self.balance_selected_row = index.row()
        self.asset_instance_in_item = self.account_balance[self.balance_selected_row]
        self.selected_asset_send.setDisabled(False)
        self.selected_asset_send.setText("Send %s to %s address"%(self.asset_instance_in_item.name, self.asset_instance_in_item.name))
        if self.asset_instance_in_item.asset_id == mixin_asset_id_collection.CNB_ASSET_ID or self.asset_instance_in_item.asset_id == mixin_asset_id_collection.XIN_ASSET_ID:
            self.selected_asset_send_to_main_net.setDisabled(False)
            self.selected_asset_send_to_main_net.setText("Send %s to Mixin address"%self.asset_instance_in_item.name)
            self.selected_asset_manageasset_mainnet.setDisabled(False)
        else:
            self.selected_asset_send_to_main_net.setDisabled(True)
            self.selected_asset_send_to_main_net.setText("Send %s to Mixin address"%self.asset_instance_in_item.name)
            self.selected_asset_manageasset_mainnet.setDisabled(True)
        self.selected_asset_manageasset.setDisabled(False)
        self.selected_asset_show_history.setDisabled(False)
        self.selected_asset_show_history.setText("Open history of " + self.asset_instance_in_item.name)
        self.asset_detail_in_balance_page.setModel(AssetDetail_TableModel(None, self.asset_instance_in_item, self.account_balance))
        self.asset_detail_in_balance_page.update()
        header = self.asset_detail_in_balance_page.verticalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header = self.asset_detail_in_balance_page.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)


    def update_asset_address_detail(self, this_withdraw_address, label_widget):
        stringForAddress = ""
        if this_withdraw_address.public_key != "":
            stringForAddress +=  ("\n" + u'Address: ' + this_withdraw_address.public_key)
        if(this_withdraw_address.account_name!= ""):
            stringForAddress += ("\n" + u'Account name:'.ljust(20) + this_withdraw_address.account_name)
        if(this_withdraw_address.account_tag!= ""):
            stringForAddress += ("\n" + u'Account tag:'.ljust(20) + this_withdraw_address.account_tag)
        if(this_withdraw_address.fee!= ""):
            stringForAddress += ("\n" + this_withdraw_address.fee + u' fee')
        if(this_withdraw_address.reserve != ""):
            stringForAddress += ("\n" + this_withdraw_address.reserve + u' reserve')
        if(this_withdraw_address.dust!= ""):
            stringForAddress += ("\n" + this_withdraw_address.dust + u' dust')
        label_widget.setText(stringForAddress)

    def clear_asset_address_detail(self, label_widget):
        label_widget.setText("")

    def withdrawaddress_list_record_selected(self, itemSelect):
        if itemSelect == None:
            return

        self.withdraw_address_instance_in_item = itemSelect.data(0x0100)
        self.update_asset_address_detail(self.withdraw_address_instance_in_item, self.withdraw_address_of_asset_detail_label)

        self.remove_address_btn.setDisabled(False)
    def mainnet_withdraw_address_list_record_selection_actived(self,itemCurr, itemPre):
        if itemCurr == None:
            self.withdraw_address_of_asset_detail_label.setText("")
            return
        self.mainnet_address_instance_in_item = itemCurr.data(0x0100)
        self.withdraw_address_of_asset_detail_label.setText("Address:%s"%(self.mainnet_address_instance_in_item.address))
        self.remove_address_btn.setDisabled(False)

    def mainnet_address_list_record_selected(self, itemSelect):
        if itemSelect == None:
            return

        self.mainnet_address_instance_in_item = itemSelect.data(0x0100)
        self.withdraw_address_of_asset_detail_label.setText("Address:%s"%(self.mainnet_address_instance_in_item.address))
        self.remove_address_btn.setDisabled(False)

    def send_withdrawaddress_list_record_indexChanged(self, indexActived):
        print("index changed %d"%indexActived)
        self.selected_withdraw_address = self.withdraw_address_of_asset_list[indexActived]
        self.update_asset_address_detail(self.selected_withdraw_address, self.send_address_title_widget)
        self.send_asset_to_withdraw_address_btn.setDisabled(False)
    def send_mainnet_withdrawaddress_list_record_indexChanged(self, indexActived):
        print("index changed %d"%indexActived)
        self.selected_mainnet_withdraw_address = self.mainnet_address_list[indexActived]
        self.send_asset_to_withdraw_address_btn.setDisabled(False)
        self.send_address_title_widget.setText("to %s !"%(self.selected_mainnet_withdraw_address.address))

    def pay_to_exin_pressed(self, base_asset, echange_asset):
        self.trade_exin_widget.close()
        memo_for_exin = exincore_api.gen_memo_ExinBuy(echange_asset)
        print("amount is %s"%self.pay_exin_amount_edit_Label_widget.text())
        print("base asset is %s"%base_asset)
        tranfer_result = self.selected_wallet_record.transfer_to(exincore_api.EXINCORE_UUID, base_asset, self.pay_exin_amount_edit_Label_widget.text(), memo_for_exin, "", self.pay_exin_pin_edit_Label_widget.text())
        if tranfer_result.is_success:
            self.update_balance()
            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Your payment to exin is successful, verify it on blockchain explorer on https://mixin.one/snapshots/%s" % tranfer_result.data.snapshot_id)
            congratulations_msg.setTextInteractionFlags(Qt.TextSelectableByMouse)
            congratulations_msg.exec_()
        else:
            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Failed to pay, reason %s" % str(tranfer_result))
            congratulations_msg.exec_()


    def send_asset_to_withdraw_address_pressed(self):
        withdraw_asset_result = self.selected_wallet_record.withdraw_asset_to(self.selected_withdraw_address.address_id, self.send_amount_edit_Label_widget.text(), "", "", self.send_pin_edit_Label_widget.text())
        if withdraw_asset_result.is_success:
            self.update_balance()
            self.send_asset_widget.close()
            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Your withdraw operation is successful, verify it on blockchain explorer on https://mixin.one/snapshots/%s" % withdraw_asset_result.data.snapshot_id)
            congratulations_msg.setTextInteractionFlags(Qt.TextSelectableByMouse)
            congratulations_msg.exec_()
        else:
            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Failed to send, reason %s" % str(withdraw_asset_result))
            congratulations_msg.exec_()

    def send_asset_to_mainnet_address_pressed(self):
        withdraw_asset_result = self.selected_wallet_record.transfer_to_mainnet(self.selected_mainnet_withdraw_address.address, self.asset_instance_in_item.asset_id, self.mainnet_send_amount_edit_Label_widget.text(), "", "", self.send_pin_edit_Label_widget.text())
        if withdraw_asset_result.is_success:
            self.update_balance()
            self.send_asset_widget.close()
            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Your withdraw operation is successful, verify it on blockchain explorer on https://mixin.one/snapshots/%s" % withdraw_asset_result.data.snapshot_id)
            self.selected_wallet_record.find_snapshot(withdraw_asset_result.data.snapshot_id)
            congratulations_msg.setTextInteractionFlags(Qt.TextSelectableByMouse)
            congratulations_msg.exec_()
        else:
            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Failed to send, reason %s" % str(withdraw_asset_result))
            congratulations_msg.exec_()


    def open_sell_trade_detail_for_exin(self):
        if (hasattr(self, "selected_exin_result")):
            self.open_trade_trade_detail_for_exin(self.selected_exin_result.echange_asset, self.selected_exin_result.base_asset)

    def open_buy_trade_detail_for_exin(self):
        if (hasattr(self, "selected_exin_result")):
            self.open_trade_trade_detail_for_exin(self.selected_exin_result.base_asset, self.selected_exin_result.echange_asset)
    def open_trade_trade_detail_for_exin(self, base_asset_id, target_asset_id):
        if (hasattr(self, "selected_exin_result")):
            asset_price_result = exincore_api.fetchExinPrice(base_asset_id, target_asset_id)
            base_asset_balance_result = self.selected_wallet_record.get_singleasset_balance(base_asset_id)
            if base_asset_balance_result.is_success:
                available_amount = base_asset_balance_result.data.balance + " in your wallet"
            else:
                available_amount = ""
            #confirm price again
            this_trade_price = asset_price_result[0]
            minimum_pay_base_asset = this_trade_price.minimum_amount
            maximum_pay_base_asset = this_trade_price.maximum_amount
            price_base_asset       = this_trade_price.price
            base_sym               = this_trade_price.base_asset_symbol
            target_sym             = this_trade_price.exchange_asset_symbol

            tradepair_price_title_label_widget = QLabel("Price:  %s %s  ==> 1 %s"%(price_base_asset, base_sym, target_sym))
            send_amount_title_widget = QLabel("Amount(min %s -> max %s) %s:%s"%(minimum_pay_base_asset, maximum_pay_base_asset, base_sym, available_amount))
            self.pay_exin_amount_edit_Label_widget = QLineEdit()
            send_pin_title_widget = QLabel("Asset pin:")
            self.pay_exin_pin_edit_Label_widget = QLineEdit()
            self.pay_exin_pin_edit_Label_widget.setMaxLength(6)
            self.pay_exin_pin_edit_Label_widget.setEchoMode(QLineEdit.Password)

            send_payment_to_exin_btn = QPushButton("Go")
            send_payment_to_exin_btn.pressed.connect(lambda :self.pay_to_exin_pressed(base_asset_id, target_asset_id))

            send_payment_to_exin_layout = QVBoxLayout()
            send_payment_to_exin_layout.addWidget(tradepair_price_title_label_widget)
            send_payment_to_exin_layout.addWidget(send_amount_title_widget)
            send_payment_to_exin_layout.addWidget(self.pay_exin_amount_edit_Label_widget)
            send_payment_to_exin_layout.addWidget(send_pin_title_widget)
            send_payment_to_exin_layout.addWidget(self.pay_exin_pin_edit_Label_widget)
            send_payment_to_exin_layout.addWidget(send_payment_to_exin_btn)

            self.trade_exin_widget = QWidget()
            self.trade_exin_widget.setLayout(send_payment_to_exin_layout)
            self.trade_exin_widget.show()
        else:
            return


    def send_asset_to_address_of_mainnet(self):
        if (hasattr(self, "asset_instance_in_item")):
            send_asset_title_label_widget = QLabel("Send " + self.asset_instance_in_item.name + " to Mixin Address")
            send_amount_title_widget = QLabel("amount, %s %s available"%(self.asset_instance_in_item.balance, self.asset_instance_in_item.symbol))
            self.mainnet_send_amount_edit_Label_widget = QLineEdit()

            send_pin_title_widget = QLabel("Asset pin:")
            self.send_pin_edit_Label_widget = QLineEdit()
            self.send_pin_edit_Label_widget.setMaxLength(6)
            self.send_pin_edit_Label_widget.setEchoMode(QLineEdit.Password)
            self.send_address_title_widget = QLabel("to ")

            self.send_address_selection_widget = QComboBox()
            Main_net_address_list = self.session.query(mixin_sqlalchemy_type.Main_net_address).all()
            self.mainnet_address_list = []

            i = 0
            for each_address in Main_net_address_list:
                self.send_address_selection_widget.insertItem(i, each_address.name, userData = each_address)
                self.mainnet_address_list.append(each_address)
                i += 1
 
            self.send_address_selection_widget.currentIndexChanged.connect(self.send_mainnet_withdrawaddress_list_record_indexChanged)
            if len(Main_net_address_list) > 0:
                self.send_address_title_widget.setText("to %s !"%self.mainnet_address_list[0].address)
                self.selected_mainnet_withdraw_address = self.mainnet_address_list[0]
            else:
                self.send_asset_to_withdraw_address_btn.setDisabled(True)
            self.send_asset_to_withdraw_address_btn = QPushButton("Send")
            self.send_asset_to_withdraw_address_btn.pressed.connect(self.send_asset_to_mainnet_address_pressed)

            send_asset_layout = QVBoxLayout()
            send_asset_layout.addWidget(send_asset_title_label_widget)
            send_asset_layout.addWidget(self.send_address_title_widget)
            send_asset_layout.addWidget(self.send_address_selection_widget)

            send_asset_layout.addWidget(send_amount_title_widget)

            send_asset_layout.addWidget(self.mainnet_send_amount_edit_Label_widget)
            send_asset_layout.addWidget(send_pin_title_widget)
            send_asset_layout.addWidget(self.send_pin_edit_Label_widget)

            send_asset_layout.addWidget(self.send_asset_to_withdraw_address_btn)
            self.send_asset_widget = QWidget()
            self.send_asset_widget.setLayout(send_asset_layout)
            self.send_asset_widget.show()

        else:
            return




    def send_asset_to_address(self):
        if (hasattr(self, "asset_instance_in_item")):
            send_asset_title_label_widget = QLabel("Send " + self.asset_instance_in_item.name + " to:")
            send_amount_title_widget = QLabel("amount, %s %s available"%(self.asset_instance_in_item.balance, self.asset_instance_in_item.symbol))
            self.send_amount_edit_Label_widget = QLineEdit()
            send_pin_title_widget = QLabel("Asset pin:")
            self.send_pin_edit_Label_widget = QLineEdit()
            self.send_pin_edit_Label_widget.setMaxLength(6)
            self.send_pin_edit_Label_widget.setEchoMode(QLineEdit.Password)
            self.send_address_title_widget = QLabel("to ")

            self.send_address_selection_widget = QComboBox()
            self.send_address_selection_widget.currentIndexChanged.connect(self.send_withdrawaddress_list_record_indexChanged)
            self.send_asset_to_withdraw_address_btn = QPushButton("Send")
            self.send_asset_to_withdraw_address_btn.pressed.connect(self.send_asset_to_withdraw_address_pressed)
            self.send_asset_to_withdraw_address_btn.setDisabled(True)

            send_asset_layout = QVBoxLayout()
            send_asset_layout.addWidget(send_asset_title_label_widget)
            send_asset_layout.addWidget(self.send_address_title_widget)
            send_asset_layout.addWidget(self.send_address_selection_widget)

            send_asset_layout.addWidget(send_amount_title_widget)

            send_asset_layout.addWidget(self.send_amount_edit_Label_widget)
            send_asset_layout.addWidget(send_pin_title_widget)
            send_asset_layout.addWidget(self.send_pin_edit_Label_widget)

            send_asset_layout.addWidget(self.send_asset_to_withdraw_address_btn)
            self.send_asset_widget = QWidget()
            self.send_asset_widget.setLayout(send_asset_layout)
            self.send_asset_widget.show()


            worker = Asset_addresses_Thread(self.selected_wallet_record, self.asset_instance_in_item)
            worker.signals.result.connect(self.received_send_withdraw_addresses_result)
            worker.signals.finished.connect(self.thread_complete)
            self.threadPool.start(worker)
        else:
            return



    def open_manage_main_net_address(self):
        if (hasattr(self, "asset_instance_in_item")):
            add_withdraw_address_asset_btn = QPushButton("Add new address")
            add_withdraw_address_asset_btn.pressed.connect(self.pop_create_mainnet_address_window_bitcoinstyle)

            self.withdraw_addresses_list_and_new_layout = QVBoxLayout()
            self.withdraw_addresses_list_and_new_layout.addWidget(add_withdraw_address_asset_btn)
            self.mainnet_withdraw_addresses_list_widget = QListWidget()
            Main_net_address_list = self.session.query(mixin_sqlalchemy_type.Main_net_address).all()

            self.mainnet_address_list = []
            for each_mainnet_address in Main_net_address_list:
                this_list_item = QListWidgetItem()
                this_list_item.setData(0x0100, each_mainnet_address)
                this_list_item.setText(each_mainnet_address.name)
                print(each_mainnet_address.name)
                self.mainnet_withdraw_addresses_list_widget.addItem(this_list_item)
                self.mainnet_address_list.append(this_list_item)

            self.mainnet_withdraw_addresses_list_widget.itemClicked.connect(self.mainnet_address_list_record_selected)
            self.mainnet_withdraw_addresses_list_widget.currentItemChanged.connect(self.mainnet_withdraw_address_list_record_selection_actived)
            self.withdraw_address_list = []


            self.withdraw_addresses_list_and_new_layout.addWidget(self.mainnet_withdraw_addresses_list_widget)


            withdraw_addresses_list_and_new_widget = QWidget()
            withdraw_addresses_list_and_new_widget.setLayout(self.withdraw_addresses_list_and_new_layout)

            self.withdraw_address_of_asset_detail_label = QLabel()
            remove_address_btn = QPushButton("Delete")
            remove_address_btn.pressed.connect(self.pop_Remove_mainnet_withdraw_address_window_bitcoinstyle)
            remove_address_btn.setDisabled(True)
            self.remove_address_btn = remove_address_btn

            withdraw_addresses_detail_layout = QVBoxLayout()


            withdraw_addresses_detail_layout.addWidget(self.withdraw_address_of_asset_detail_label)
            withdraw_addresses_detail_layout.addWidget(remove_address_btn)

            withdraw_addresses_detail_widget = QWidget()
            withdraw_addresses_detail_widget.setLayout(withdraw_addresses_detail_layout)
            withdraw_addresses_list_and_new_detail_layout = QHBoxLayout()
            withdraw_addresses_list_and_new_detail_layout.addWidget(withdraw_addresses_list_and_new_widget)
            withdraw_addresses_list_and_new_detail_layout.addWidget(withdraw_addresses_detail_widget)
            self.withdraw_addresses_list_and_new_detail_Widget = QWidget()
            self.withdraw_addresses_list_and_new_detail_Widget.setLayout(withdraw_addresses_list_and_new_detail_layout)
            self.withdraw_addresses_list_and_new_detail_Widget.show()
        else:
            return



    def open_widget_manage_asset(self):
        if (hasattr(self, "asset_instance_in_item")):
            
            add_withdraw_address_asset_btn = QPushButton("Add new address")
            if(self.asset_instance_in_item.chain_id == mixin_asset_id_collection.EOS_ASSET_ID):
                add_withdraw_address_asset_btn.pressed.connect(self.pop_create_withdraw_address_window_eosstyle)
            else:
                add_withdraw_address_asset_btn.pressed.connect(self.pop_create_withdraw_address_window_bitcoinstyle)

            self.withdraw_addresses_list_and_new_layout = QVBoxLayout()
            self.withdraw_addresses_list_and_new_layout.addWidget(add_withdraw_address_asset_btn)
            self.withdraw_addresses_list_widget = QListWidget()
            self.withdraw_addresses_list_widget.itemClicked.connect(self.withdrawaddress_list_record_selected)
            self.withdraw_addresses_list_widget.currentItemChanged.connect(self.withdraw_address_list_record_selection_actived)
            self.withdraw_address_list = []


            self.withdraw_addresses_list_and_new_layout.addWidget(self.withdraw_addresses_list_widget)


            withdraw_addresses_list_and_new_widget = QWidget()
            withdraw_addresses_list_and_new_widget.setLayout(self.withdraw_addresses_list_and_new_layout)

            self.withdraw_address_of_asset_detail_label = QLabel()
            remove_address_btn = QPushButton("Delete")
            remove_address_btn.pressed.connect(self.pop_Remove_withdraw_address_window_bitcoinstyle)
            remove_address_btn.setDisabled(True)
            self.remove_address_btn = remove_address_btn

            withdraw_addresses_detail_layout = QVBoxLayout()


            withdraw_addresses_detail_layout.addWidget(self.withdraw_address_of_asset_detail_label)
            withdraw_addresses_detail_layout.addWidget(remove_address_btn)

            withdraw_addresses_detail_widget = QWidget()
            withdraw_addresses_detail_widget.setLayout(withdraw_addresses_detail_layout)
            withdraw_addresses_list_and_new_detail_layout = QHBoxLayout()
            withdraw_addresses_list_and_new_detail_layout.addWidget(withdraw_addresses_list_and_new_widget)
            withdraw_addresses_list_and_new_detail_layout.addWidget(withdraw_addresses_detail_widget)
            self.withdraw_addresses_list_and_new_detail_Widget = QWidget()
            self.withdraw_addresses_list_and_new_detail_Widget.setLayout(withdraw_addresses_list_and_new_detail_layout)
            self.withdraw_addresses_list_and_new_detail_Widget.show()

            worker = Asset_addresses_Thread(self.selected_wallet_record, self.asset_instance_in_item)
            worker.signals.result.connect(self.received_asset_withdraw_addresses_result)
            worker.signals.finished.connect(self.thread_complete)
            self.threadPool.start(worker)
        else:
            return


    def received_ocean_result(self, oceanResult):
        if hasattr(oceanResult, "timestamp"):
            ocean_target_asset_selection_asset = self.get_ocean_target_asset_selection_asset()
            if ocean_target_asset_selection_asset != None:
                quote_asset = self.get_ocean_quote_asset_selection_asset()
                ask_order_model = OceanOrder_TableModel(None, reversed(oceanResult.ask_order_list), ["Ask price in " + quote_asset[0], "Ask " + ocean_target_asset_selection_asset.asset_symbol + " amount", "Funds in " + quote_asset[0]])
            self.ocean_order_ask_book_widget.setModel(ask_order_model)
            self.ocean_order_ask_book_widget.update()
            self.ocean_order_ask_book_widget.selectRow(len(oceanResult.ask_order_list) - 1)

            bid_order_model = OceanOrder_TableModel(None, oceanResult.bid_order_list, ["Bid price", "Amount", "Funds"])
            self.ocean_order_bid_book_widget.setModel(bid_order_model)
            self.ocean_order_bid_book_widget.update()
            self.ocean_order_bid_book_widget.selectRow(0)
        else:
            ask_order_model = OceanOrder_TableModel(None, [])
            self.ocean_order_ask_book_widget.setModel(ask_order_model)
            self.ocean_order_ask_book_widget.update()

            bid_order_model = OceanOrder_TableModel(None, [])
            self.ocean_order_bid_book_widget.setModel(bid_order_model)
            self.ocean_order_bid_book_widget.update()

    def fetchOceanPrice(self):
        if self.ocean_target_asset_id_input.text() != "":
            quote_asset = self.get_ocean_quote_asset_selection_asset()
            ocean_worker = Ocean_Thread(quote_asset[1], self.ocean_target_asset_id_input.text())
            update_asset_name_worker = ReadAsset_Info_Thread(self.selected_wallet_record, self.ocean_target_asset_id_input.text())
            update_asset_name_worker.signals.result.connect(self.received_asset_balance)
            self.threadPool.start(update_asset_name_worker)

        else:
            ocean_target_asset_selection_asset = self.get_ocean_target_asset_selection_asset()
            if ocean_target_asset_selection_asset != None:
                quote_asset = self.get_ocean_quote_asset_selection_asset()
                ocean_worker = Ocean_Thread(quote_asset[1], ocean_target_asset_selection_asset.asset_id)
                ocean_worker.signals.result.connect(self.received_ocean_result)
                #ocean_worker.signals.finished.connect(self.thread_complete)
                self.threadPool.start(ocean_worker)

    def reload_ocean_target_selection_asset(self):
        self.quote_target_asset_selection.clear()
        known_asset_list = self.known_assets()
        i = 0
        self.ocean_target_id_name = []
        for each in known_asset_list:
            self.quote_target_asset_selection.insertItem(i, each.asset_symbol + " asset", each.asset_id)
            self.ocean_target_id_name.append(each)
            i += 1

    def get_ocean_quote_asset_selection_asset(self):
        current_selection = self.quote_asset_selection.currentIndex()
        if current_selection >= 0 and current_selection < len(self.ocean_id_name):
            return self.ocean_id_name[current_selection]
        else:
            return None


    def get_ocean_target_asset_selection_asset(self):
        current_selection = self.quote_target_asset_selection.currentIndex()
        if current_selection >= 0 and current_selection < len(self.ocean_target_id_name):
            return self.ocean_target_id_name[current_selection]
        else:
            return None

    def ocean_base_asset_change(self, indexActived):
        quote_asset = self.get_ocean_quote_asset_selection_asset()

        ocean_target_asset_selection_asset = self.get_ocean_target_asset_selection_asset()
        if ocean_target_asset_selection_asset != None:
            self.price_unit.setText(quote_asset[0] + " per " + ocean_target_asset_selection_asset.asset_symbol)


        self.ocean_target_asset_amount_input.setPlaceholderText("%s amount"%(quote_asset[0]))
        update_asset_balance_worker = ReadAsset_Info_Thread(self.selected_wallet_record, quote_asset[1])
        update_asset_balance_worker.signals.result.connect(self.update_ocean_pay_amount_base)
        self.threadPool.start(update_asset_balance_worker)

        self.ocean_target_asset_price_input.setPlaceholderText("Mininum price " + quote_asset[2])


        self.fetchOceanPrice()

    def ocean_target_asset_change(self, indexActived):
        print("indexActived%d"%indexActived)
        ocean_target_asset_selection_asset = self.get_ocean_target_asset_selection_asset()
        if ocean_target_asset_selection_asset != None:
            quote_asset = self.get_ocean_quote_asset_selection_asset()
            self.price_unit.setText(quote_asset[0] + " per " + ocean_target_asset_selection_asset.asset_symbol)
            self.ocean_buy_btn.setText("Buy "+ ocean_target_asset_selection_asset.asset_symbol)
            self.ocean_sell_btn.setText("Sell "+ ocean_target_asset_selection_asset.asset_symbol)
            self.ocean_target_asset_sell_amount_input.setPlaceholderText("%s amount"%(ocean_target_asset_selection_asset.asset_symbol))

            update_asset_balance_worker = ReadAsset_Info_Thread(self.selected_wallet_record, ocean_target_asset_selection_asset.asset_id)
            update_asset_balance_worker.signals.result.connect(self.update_ocean_pay_amount_target)
            self.threadPool.start(update_asset_balance_worker)
            self.fetchOceanPrice()

    def received_asset_balance(self, asset):
        if asset.is_success:
            self.add_asset_into_localdb_if_never_see(asset.data)

    def fetch_asset_symbol_from_asset_id(self, asset_id_string):
        known_assets = self.session.query(mixin_sqlalchemy_type.Mixin_asset_record).filter_by(asset_id = asset_id_string).all()
        if len(known_assets) == 0:
            #fetch asset by thread
            return None
        else:
            #found asset
            return known_assets[0].asset_name

    def update_ocean_pay_amount_base(self, asset_info):
        print("ocean pay amount base is finished for %s"%asset_info.data.symbol)
        if asset_info.is_success:
            self.ocean_target_asset_amount_input.setPlaceholderText("%s amount, %s in wallet"%(asset_info.data.symbol, asset_info.data.balance))
        return
    def update_ocean_pay_amount_target(self, asset_info):
        if asset_info.is_success:
            self.ocean_target_asset_sell_amount_input.setPlaceholderText("%s amount, %s in wallet"%(asset_info.data.symbol, asset_info.data.balance))
            if hasattr(self, "account_balance"):
                self.asset_detail_in_ocean_page.setModel(AssetIntro_TableModel(None, asset_info.data, self.account_balance))
                self.asset_detail_in_ocean_page.update()
                header = self.asset_detail_in_ocean_page.verticalHeader()       
                header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
                header = self.asset_detail_in_ocean_page.horizontalHeader()       
                header.setSectionResizeMode(0, QHeaderView.ResizeToContents)


        return
    def known_assets(self):
        know_asset_id_name_groups = self.session.query(mixin_sqlalchemy_type.Mixin_asset_record).order_by(mixin_sqlalchemy_type.Mixin_asset_record.id.asc()).all()
        know_id_groups = []
        for each in know_asset_id_name_groups:
            know_id_groups.append(each.asset_id)
        for default_id in mixin_asset_id_collection.MIXIN_DEFAULT_CHAIN_GROUP:
            if not (default_id in know_asset_id_name_groups):
                update_asset_name_worker = ReadAsset_Info_Thread(self.selected_wallet_record, default_id)
                update_asset_name_worker.signals.result.connect(self.received_asset_balance)
                self.threadPool.start(update_asset_name_worker)
        return know_asset_id_name_groups

    def ocean_price_changed(self, changedText):
        print(changedText)
        try:
            price  = float(changedText)
            amount = float(self.ocean_target_asset_amount_input.text())
            if amount > 0 and price > 0:
                ocean_target_asset_selection_asset = self.get_ocean_target_asset_selection_asset()
                if ocean_target_asset_selection_asset != None:
                    self.order_funds_label.setText("%s %s"%(str(amount/price), ocean_target_asset_selection_asset.asset_symbol))
            amount = float(self.ocean_target_asset_sell_amount_input.text())
            if amount > 0 and price > 0:
                quote_asset = self.get_ocean_quote_asset_selection_asset()
                self.order_funds_sell_label.setText("%s %s"%(str(amount/price), quote_asset[0]))
        except ValueError:
            return

    def ocean_amount_change(self, changedText):
        try:
            amount = float(changedText)
            price = float(self.ocean_target_asset_price_input.text())
            if amount > 0 and price > 0:
                ocean_target_asset_selection_asset = self.get_ocean_target_asset_selection_asset()
                if ocean_target_asset_selection_asset != None:
                    self.order_funds_label.setText("%s %s"%(str(amount/price), ocean_target_asset_selection_asset.asset_symbol))
        except ValueError:
            return

    def mixin_node_change(self, changedText):
        try:
            totalNodes = int(changedText)

            self.maximum_failed_node_mixin_label.setText("Mixin Network can still work even %d node stopped"%(wallet_api.minimum_nodes_attack_mixin(totalNodes) - 1))
            minimum_value_to_stop_text = "The minimum cost to stop Mixin Network is %d xin token"%(wallet_api.minimum_nodes_attack_mixin(totalNodes)* 10000)

            minimum_value_to_control_text = "The cost to control Mixin Network is %d XIN token"%(wallet_api.minimum_nodes_control_mixin(totalNodes) * 10000)
            if hasattr(self, "xin_token_price"):
                minimum_usd_to_stop = wallet_api.minimum_nodes_attack_mixin(totalNodes)* 10000 * float(self.xin_token_price)
                minimum_value_to_stop_text += " , about "
                minimum_value_to_stop_text += "{:,}".format(minimum_usd_to_stop)
                minimum_value_to_stop_text += " USD"

                minimum_usd_to_control = wallet_api.minimum_nodes_control_mixin(totalNodes)* 10000 * float(self.xin_token_price)
                minimum_value_to_control_text += ", about "
                minimum_value_to_control_text += "{:,}".format(minimum_usd_to_control)
                minimum_value_to_control_text += " USD"

            self.minimum_node_to_stop_mixin_label.setText(minimum_value_to_stop_text)
            self.minimum_node_to_control_mixin_label.setText(minimum_value_to_control_text)
        except ValueError:
            return
    def ocean_sell_amount_change(self, changedText):
        try:
            amount = float(changedText)
            price = float(self.ocean_target_asset_price_input.text())
            if amount > 0 and price > 0:
                quote_asset = self.get_ocean_quote_asset_selection_asset()
                self.order_funds_sell_label.setText("%s %s"%(str(amount*price), quote_asset[0]))

        except ValueError:
            return

    def ocean_reg_key_btn_pressed(self):

        current_input_pin    = self.ocean_reg_key_pin.text()
        asset_id_for_regkey = self.asset_to_reg_key.asset_id
        sk = oceanone_api.generateECDSAKey()
        vk = oceanone_api.export_pubKey_fromPrivateKey(sk)
        vk_in_string = oceanone_api.key_to_string(vk)
        memo_to_ocean = oceanone_api.gen_memo_ocean_reg_key(vk_in_string)
        print([current_input_pin, asset_id_for_regkey, memo_to_ocean])
        tranfer_result = self.selected_wallet_record.transfer_to(oceanone_api.OCEANONE_UUID, asset_id_for_regkey, "0.00001", memo_to_ocean, "", current_input_pin)
        if tranfer_result.is_success:
            self.update_balance()
            with open(self.file_name+".oceanonekey", "wb") as oceanonekeyfile:
                oceanonekeyfile.write(base64.b64encode(oceanone_api.key_to_string(sk)))

            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Your payment to ocean is successful, verify it on blockchain explorer on https://mixin.one/snapshots/%s" % tranfer_result.data.snapshot_id)
            congratulations_msg.setTextInteractionFlags(Qt.TextSelectableByMouse)
            congratulations_msg.exec_()
        else:
            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Failed to pay, reason %s" % str(tranfer_result))
            congratulations_msg.exec_()


    def ocean_cancel_order_btn_pressed(self):

        current_input_pin    = self.ocean_cancel_order_pin.text()
        this_trade = self.ocean_history_list[self.ocean_history_selected_row].order_id
        asset_id_for_cancel = self.asset_to_cancel_ocean_order.asset_id
        memo_to_ocean = oceanone_api.gen_memo_ocean_cancel_order(this_trade)
        print([current_input_pin, this_trade, asset_id_for_cancel, memo_to_ocean])
        tranfer_result = self.selected_wallet_record.transfer_to(oceanone_api.OCEANONE_UUID, asset_id_for_cancel, "0.00000001", memo_to_ocean, "", current_input_pin)
        if tranfer_result.is_success:
            new_ocean_trade = mixin_sqlalchemy_type.Ocean_trade_record()
            new_ocean_trade.pay_asset_id = asset_id_for_cancel
            new_ocean_trade.pay_asset_amount   = "0.00000001"
            new_ocean_trade.asset_id     = ""
            new_ocean_trade.price        ="" 
            new_ocean_trade.operation_type = ""
            new_ocean_trade.side           = ""
            new_ocean_trade.order_id       = ""
            self.session.add(new_ocean_trade)
            self.session.commit()

            self.update_balance()
            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Your payment to ocean is successful, verify it on blockchain explorer on https://mixin.one/snapshots/%s" % tranfer_result.data.snapshot_id)
            congratulations_msg.setTextInteractionFlags(Qt.TextSelectableByMouse)
            congratulations_msg.exec_()
        else:
            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Failed to pay, reason %s" % str(tranfer_result))
            congratulations_msg.exec_()


    def register_key_to_oceanone(self):
        self.ocean_reg_key_btn = QPushButton("Pay 0.00000001 to register your local key" + self.file_name + ".oceanonekey")
        self.ocean_reg_key_btn.pressed.connect(self.ocean_reg_key_btn_pressed)

        self.ocean_reg_key_pin = QLineEdit()
        self.ocean_reg_key_pin.setPlaceholderText("Asset pin")

        self.non_zero_asset_list = []

        ocean_reg_key_layout = QVBoxLayout()
        for each in self.account_balance:
            if each.balance != "0":
                self.non_zero_asset_list.append(each)
        if len(self.non_zero_asset_list) > 0:
            reg_key_pay_asset_combo = QComboBox()
            reg_key_pay_asset_combo.currentIndexChanged.connect(self.ocean_reg_key_asset_changed)
            self.asset_to_reg_key= self.non_zero_asset_list[0]
            i = 0
            for each in self.non_zero_asset_list:
                reg_key_pay_asset_combo.addItem(each.symbol)

            ocean_reg_key_layout.addWidget(reg_key_pay_asset_combo)
        ocean_reg_key_layout.addWidget(self.ocean_reg_key_pin)
        ocean_reg_key_layout.addWidget(self.ocean_reg_key_btn)

        self.ocean_reg_key_widget = QWidget()
        self.ocean_reg_key_widget.setLayout(ocean_reg_key_layout)
        self.ocean_reg_key_widget.show()
 
    def ocean_open_cloud_history(self):
        print(oceanone_api.load_my_order(self.selected_wallet_record.userid, self.selected_wallet_record.session_id, self.oceanone_key_in_pem))

    def ocean_open_history(self):
        ocean_history_list = self.session.query(mixin_sqlalchemy_type.Ocean_trade_record).all()
        self.ocean_history_list = []
        for each_record_ocean in ocean_history_list:
            print(each_record_ocean.order_id)
            if each_record_ocean.order_id != None and each_record_ocean.order_id != "":
                self.ocean_history_list.append(each_record_ocean)
        this_table_model = OceanHistoryTableModel(None, self.ocean_history_list, ["Pay Asset", "Pay amount", "Target asset", "Price", "Operation", "Side", "Order_id"])
        self.ocean_cancel_order_btn = QPushButton("Cancel")
        self.ocean_cancel_order_btn.pressed.connect(self.ocean_cancel_order_btn_pressed)

        self.ocean_cancel_order_label = QLabel()

        self.ocean_cancel_order_pin = QLineEdit()
        self.ocean_cancel_order_pin.setPlaceholderText("Asset pin")
        self.ocean_cancel_order_pin.setMaxLength(6)
        self.ocean_cancel_order_pin.setEchoMode(QLineEdit.Password)

        ocean_history_table = QTableView()
        ocean_history_table.setModel(this_table_model)
        ocean_history_table.clicked.connect(self.ocean_list_record_selected)
        ocean_history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        header = ocean_history_table.horizontalHeader()       
        if len(self.ocean_history_list) > 0:
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(6, QHeaderView.ResizeToContents)


        if len(self.ocean_history_list) > 0:
            ocean_history_table.selectRow(0)
        self.ocean_history_selected_row = 0

        self.non_zero_asset_list = []

        ocean_history_layout = QVBoxLayout()
        for each in self.account_balance:
            if each.balance != "0":
                self.non_zero_asset_list.append(each)
        if len(self.non_zero_asset_list) > 0:
            cancel_order_pay_asset_combo = QComboBox()
            cancel_order_pay_asset_combo.currentIndexChanged.connect(self.ocean_cancel_order_asset_changed)
            self.asset_to_cancel_ocean_order = self.non_zero_asset_list[0]
            i = 0
            for each in self.non_zero_asset_list:
                cancel_order_pay_asset_combo.addItem(each.name + each.balance + each.symbol)

            ocean_history_layout.addWidget(cancel_order_pay_asset_combo)
        else:
            self.asset_to_cancel_ocean_order = None 
            self.ocean_cancel_order_btn.setDisabled(True)

        ocean_history_layout.addWidget(self.ocean_cancel_order_pin)

        ocean_history_layout.addWidget(self.ocean_cancel_order_label)
        ocean_history_layout.addWidget(self.ocean_cancel_order_btn)

        ocean_history_layout.addWidget(ocean_history_table)
        self.ocean_history_widget = QWidget()
        self.ocean_history_widget.setLayout(ocean_history_layout)
        self.ocean_history_widget.show()
        
    def ocean_make_sell_order(self):
        quote_asset = self.get_ocean_quote_asset_selection_asset()
        current_base_asset   = quote_asset[1]
        ocean_target_asset_selection_asset = self.get_ocean_target_asset_selection_asset()
        if ocean_target_asset_selection_asset == None:
            return
        current_target_asset = ocean_target_asset_selection_asset.asset_id
        current_amount       = self.ocean_target_asset_sell_amount_input.text()
        current_price        = self.ocean_target_asset_price_input.text()
        current_input_pin    = self.ocean_pin_input.text()
        current_uuid         = str(uuid.uuid1())
        memo_to_ocean = oceanone_api.gen_memo_ocean_ask(current_base_asset, current_price)
        tranfer_result = self.selected_wallet_record.transfer_to(oceanone_api.OCEANONE_UUID, current_target_asset, current_amount, memo_to_ocean, current_uuid, current_input_pin)
        if tranfer_result.is_success:
            new_ocean_trade = mixin_sqlalchemy_type.Ocean_trade_record()
            new_ocean_trade.pay_asset_id = current_base_asset
            new_ocean_trade.pay_asset_amount   = current_amount
            new_ocean_trade.asset_id     = current_target_asset
            new_ocean_trade.price        = current_price
            new_ocean_trade.operation_type = "L"
            new_ocean_trade.side           = "B"
            new_ocean_trade.order_id       = current_uuid
            self.session.add(new_ocean_trade)
            self.session.commit()

            self.update_balance()
            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Your payment to ocean is successful, verify it on blockchain explorer on https://mixin.one/snapshots/%s" % tranfer_result.data.snapshot_id)
            congratulations_msg.setTextInteractionFlags(Qt.TextSelectableByMouse)
            congratulations_msg.exec_()
        else:
            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Failed to pay, reason %s" % str(tranfer_result))
            congratulations_msg.exec_()


    def ocean_make_buy_order(self):
        quote_asset = self.get_ocean_quote_asset_selection_asset()
        current_base_asset   = quote_asset[1]
        ocean_target_asset_selection_asset = self.get_ocean_target_asset_selection_asset()
        if ocean_target_asset_selection_asset == None:
            return
        current_target_asset = ocean_target_asset_selection_asset.asset_id
        current_amount       = self.ocean_target_asset_amount_input.text()
        current_price        = self.ocean_target_asset_price_input.text()
        current_input_pin    = self.ocean_pin_input.text()
        current_uuid         = str(uuid.uuid1())
        memo_to_ocean = oceanone_api.gen_memo_ocean_bid(current_target_asset, current_price)
        tranfer_result = self.selected_wallet_record.transfer_to(oceanone_api.OCEANONE_UUID, current_base_asset, current_amount, memo_to_ocean, current_uuid, current_input_pin)
        if tranfer_result.is_success:
            new_ocean_trade = mixin_sqlalchemy_type.Ocean_trade_record()
            new_ocean_trade.pay_asset_id = current_base_asset
            new_ocean_trade.pay_asset_amount   = current_amount
            new_ocean_trade.asset_id     = current_target_asset
            new_ocean_trade.price        = current_price
            new_ocean_trade.operation_type = "L"
            new_ocean_trade.side           = "B"
            new_ocean_trade.order_id       = current_uuid
            self.session.add(new_ocean_trade)
            self.session.commit()

            self.update_balance()
            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Your payment to ocean is successful, verify it on blockchain explorer on https://mixin.one/snapshots/%s" % tranfer_result.data.snapshot_id)
            congratulations_msg.setTextInteractionFlags(Qt.TextSelectableByMouse)
            congratulations_msg.exec_()
        else:
            congratulations_msg = QMessageBox()
            congratulations_msg.setText("Failed to pay, reason %s" % str(tranfer_result))
            congratulations_msg.exec_()


    def create_ocean_exchange_widget(self):
        self.ocean_order_ask_book_widget = QTableView()
        self.ocean_order_bid_book_widget = QTableView()

        self.ocean_id_name = [("USDT", mixin_asset_id_collection.USDT_ASSET_ID, "0.0001"), ("XIN", mixin_asset_id_collection.XIN_ASSET_ID, "0.00000001"), ("BTC", mixin_asset_id_collection.BTC_ASSET_ID, "0.00000001")] 

        self.quote_asset_selection = QComboBox()

        i = 0
        for each in self.ocean_id_name:
            self.quote_asset_selection.insertItem(i, each[0] + " Market", each[0])
            i += 1
        self.quote_asset_selection.currentIndexChanged.connect(self.ocean_base_asset_change)

        self.quote_target_asset_selection = QComboBox()
        self.reload_ocean_target_selection_asset()
        self.quote_target_asset_selection.currentIndexChanged.connect(self.ocean_target_asset_change)
        self.ocean_target_asset_id_input = QLineEdit()
        self.ocean_target_asset_id_input.setPlaceholderText("Asset id")

        quote_layout = QHBoxLayout()
        quote_layout.addWidget(self.quote_asset_selection)
        quote_layout.addWidget(self.quote_target_asset_selection)
        reload_ocean_target_btn = QPushButton("load more")
        reload_ocean_target_btn.pressed.connect(self.reload_ocean_target_selection_asset)
        quote_layout.addWidget(reload_ocean_target_btn)
        quote_widget = QWidget()
        quote_widget.setLayout(quote_layout)


        operation_this_layout = QVBoxLayout()
        operation_this_layout.addWidget(quote_widget)

        self.asset_detail_in_ocean_page = QTableView()

        operation_this_layout.addWidget(self.ocean_target_asset_id_input)
        operation_this_layout.addWidget(self.asset_detail_in_ocean_page)

        fetchOceanPriceBtn = QPushButton("Load order")
        fetchOceanPriceBtn.pressed.connect(self.fetchOceanPrice)
        operation_this_layout.addWidget(fetchOceanPriceBtn)

        make_order_layout = QVBoxLayout()
        self.ocean_target_asset_amount_input = QLineEdit()
        self.ocean_target_asset_amount_input.textChanged.connect(self.ocean_amount_change)
        self.ocean_target_asset_sell_amount_input = QLineEdit()
        self.ocean_target_asset_sell_amount_input.textChanged.connect(self.ocean_sell_amount_change)

        self.ocean_target_asset_price_input = QLineEdit()
        self.ocean_target_asset_price_input.setPlaceholderText("Price")
        self.ocean_target_asset_price_input.textChanged.connect(self.ocean_price_changed)
        self.ocean_target_asset_price_input.setPlaceholderText("Mininum price " + self.ocean_id_name[0][2])

        self.ocean_pin_input = QLineEdit()
        self.ocean_pin_input.setPlaceholderText("Asset pin")
        self.ocean_pin_input.setEchoMode(QLineEdit.Password)
        self.ocean_pin_input.setMaxLength(6)



        price_layout = QHBoxLayout()
        self.price_unit = QLabel()

        price_layout.addWidget(self.ocean_target_asset_price_input)
        price_layout.addWidget(self.price_unit)
        price_widget = QWidget()
        price_widget.setLayout(price_layout)

        amount_layout = QHBoxLayout()
        amount_layout.addWidget(self.ocean_target_asset_amount_input)

        amount_sell_layout = QHBoxLayout()
        amount_sell_layout.addWidget(self.ocean_target_asset_sell_amount_input)

        quote_asset = self.get_ocean_quote_asset_selection_asset()
        self.ocean_target_asset_amount_input.setPlaceholderText("% amount"%quote_asset[0])
        update_asset_balance_worker = ReadAsset_Info_Thread(self.selected_wallet_record, quote_asset[1])
        update_asset_balance_worker.signals.result.connect(self.update_ocean_pay_amount_base)
        self.threadPool.start(update_asset_balance_worker)


        amount_widget = QWidget()
        amount_widget.setLayout(amount_layout)
        amount_sell_widget = QWidget()
        amount_sell_widget.setLayout(amount_sell_layout)


        self.ocean_buy_btn = QPushButton("Buy ")
        self.ocean_buy_btn.pressed.connect(self.ocean_make_buy_order)
        self.ocean_sell_btn = QPushButton("Sell")
        self.ocean_sell_btn.pressed.connect(self.ocean_make_sell_order)
        if len(self.ocean_target_id_name):
            ocean_target_asset_selection_asset = self.get_ocean_target_asset_selection_asset()
            if ocean_target_asset_selection_asset != None:
                quote_asset = self.get_ocean_quote_asset_selection_asset()
                self.price_unit.setText(quote_asset[0] + " per " + ocean_target_asset_selection_asset.asset_symbol)
            self.ocean_target_asset_sell_amount_input.setPlaceholderText("% amount"%self.ocean_target_id_name[0].asset_symbol)
            update_asset_balance_worker = ReadAsset_Info_Thread(self.selected_wallet_record, self.ocean_target_id_name[0].asset_id)
            update_asset_balance_worker.signals.result.connect(self.update_ocean_pay_amount_target)
            self.threadPool.start(update_asset_balance_worker)
            self.ocean_buy_btn.setText("Buy "+ self.ocean_target_id_name[0].asset_symbol)
            self.ocean_sell_btn.setText("Sell " + self.ocean_target_id_name[0].asset_symbol)

        history_btn = QPushButton("Ocean history in local wallet")
        history_btn.pressed.connect(self.ocean_open_history)



        self.order_funds_label = QLabel("")

        self.order_funds_sell_label = QLabel("")

        buy_operation_layout = QVBoxLayout()
        buy_operation_layout.addWidget(amount_widget)
        buy_operation_layout.addWidget(self.order_funds_label)
        buy_operation_layout.addWidget(self.ocean_buy_btn)
        buy_operation_widget = QWidget()
        buy_operation_widget.setLayout(buy_operation_layout)
        sell_operation_layout = QVBoxLayout()
        sell_operation_layout.addWidget(amount_sell_widget)
        sell_operation_layout.addWidget(self.order_funds_sell_label)
        sell_operation_layout.addWidget(self.ocean_sell_btn)
        sell_operation_widget = QWidget()
        sell_operation_widget.setLayout(sell_operation_layout)


        action_btn_tab_widget = QTabWidget()
        action_btn_tab_widget.addTab(buy_operation_widget, "Buy")
        action_btn_tab_widget.addTab(sell_operation_widget, "Sell")

        make_order_layout.addWidget(price_widget)


        make_order_layout.addWidget(self.ocean_pin_input)
        make_order_layout.addWidget(action_btn_tab_widget)

        make_order_layout.addWidget(history_btn)
        """
        if os.path.isfile(self.file_name+".oceanonekey"):
            with open(self.file_name+".oceanonekey") as oceanonekeyfile:
                oceanone_key_in_string = base64.b64decode(oceanonekeyfile.read())
                sk = oceanone_api.loadECDSAKey_fromString(oceanone_key_in_string)
                self.oceanone_key_in_pem = sk.to_pem().decode('utf8')
                registered_btn = QPushButton("Load my order from OceanOne server")
                registered_btn.pressed.connect(self.ocean_open_cloud_history)
                make_order_layout.addWidget(registered_btn)

        else:
            registered_btn = QPushButton("Register a key to OceanOne to find your order")
            registered_btn.pressed.connect(self.register_key_to_oceanone)
            make_order_layout.addWidget(registered_btn)
        """
        make_order_widget = QWidget()
        make_order_widget.setLayout(make_order_layout)

        operation_detail = QWidget() 
        operation_detail.setLayout(operation_this_layout)

        right_side_layout = QVBoxLayout()
        right_side_layout.addWidget(operation_detail)
        right_side_layout.addWidget(make_order_widget)
        right_side_widget = QWidget()
        right_side_widget.setLayout(right_side_layout)



        order_book_layout = QVBoxLayout()
        order_book_layout.addWidget(self.ocean_order_ask_book_widget)
        order_book_layout.addWidget(self.ocean_order_bid_book_widget)
        order_book_layout.setAlignment(Qt.AlignCenter)
        order_book_widget = QWidget()
        order_book_widget.setLayout(order_book_layout)
        final_widget = QWidget()
        final_layout = QHBoxLayout()
        final_widget.setLayout(final_layout)

        final_layout.addWidget(order_book_widget)
        final_layout.addWidget(right_side_widget)

        return final_widget


    def create_exin_exchange_widget(self):
        self.selected_trade_buy_btn = QPushButton("Buy")
        self.selected_trade_buy_btn.pressed.connect(self.open_buy_trade_detail_for_exin)
        self.selected_trade_buy_btn.setDisabled(True)

        self.selected_trade_sell_btn= QPushButton("Sell")
        self.selected_trade_sell_btn.pressed.connect(self.open_sell_trade_detail_for_exin)
        self.selected_trade_sell_btn.setDisabled(True)



        self.exin_tradelist_layout = QVBoxLayout()
        self.exin_tradelist_widget = QTableView()

        self.exin_tradelist_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.exin_tradelist_widget.clicked.connect(self.exin_trade_list_record_selected)

        self.exin_tradelist_and_detail_layout = QVBoxLayout()
        self.exin_tradelist_and_detail_layout.addWidget(self.exin_tradelist_widget)
        self.exin_tradelist_and_detail_widget = QWidget()
        self.exin_tradelist_and_detail_widget.setLayout(self.exin_tradelist_and_detail_layout)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.selected_trade_buy_btn)
        button_layout.addWidget(self.selected_trade_sell_btn)
        button_group_widget = QWidget()
        button_group_widget.setLayout(button_layout)

        this_layout = QVBoxLayout()
        this_layout.addWidget(button_group_widget)
        this_layout.addWidget(self.exin_tradelist_and_detail_widget)
        exin_title_trade_list_detail = QWidget()
        exin_title_trade_list_detail.setLayout(this_layout)
        return exin_title_trade_list_detail


    def pop_deposit_addess_of_asset(self):
        if (hasattr(self, "asset_instance_in_item")):
            congratulations_msg = QMessageBox()
            deposit_address_title_value_segments = self.asset_instance_in_item.deposit_address()
            first_seg = deposit_address_title_value_segments[0]
            deposit_label_content = first_seg["title"] + " : " + first_seg["value"]

            if len(deposit_address_title_value_segments) > 1:
                second_seg = deposit_address_title_value_segments[1]
                deposit_label_content += "\n" + second_seg["title"] + " : " + second_seg["value"]
         
            congratulations_msg.setText(deposit_label_content)
            congratulations_msg.setTextInteractionFlags(Qt.TextSelectableByMouse)
            congratulations_msg.exec_()

    def create_balance_widget(self):
        self.selected_asset_send = QPushButton("Send")
        self.selected_asset_send.setDisabled(True)
        self.selected_asset_send.pressed.connect(self.send_asset_to_address)
        self.selected_asset_send_to_main_net = QPushButton("Send to Main Net")
        self.selected_asset_send_to_main_net.setDisabled(True)
        self.selected_asset_send_to_main_net.pressed.connect(self.send_asset_to_address_of_mainnet)

        self.selected_asset_manageasset = QPushButton("Manage contact")
        self.selected_asset_manageasset.setDisabled(True)
        self.selected_asset_manageasset.pressed.connect(self.open_widget_manage_asset)
        self.selected_asset_manageasset_mainnet = QPushButton("Manage contact for Mixin Main net")
        self.selected_asset_manageasset_mainnet.setDisabled(True)
        self.selected_asset_manageasset_mainnet.pressed.connect(self.open_manage_main_net_address)

        self.selected_asset_show_history = QPushButton("History")
        self.selected_asset_show_history.pressed.connect(self.open_asset_transaction_history)
        self.selected_asset_show_history.setDisabled(True)


        asset_operation_layout = QVBoxLayout()
        asset_operation_layout.addWidget(self.selected_asset_send)
        asset_operation_layout.addWidget(self.selected_asset_manageasset)
        asset_operation_layout.addWidget(self.selected_asset_show_history)

        asset_operation_layout.addWidget(self.selected_asset_send_to_main_net)
        asset_operation_layout.addWidget(self.selected_asset_manageasset_mainnet)

        self.balance_list_tableview = QTableView()
        self.balance_list_tableview.clicked.connect(self.balance_list_record_selected)

        asset_operation_widget = QWidget()
        asset_operation_widget.setLayout(asset_operation_layout)

        self.asset_detail_in_balance_page = QTableView()

        asset_detail_operation_layout = QVBoxLayout()
        asset_detail_operation_layout.addWidget(self.asset_detail_in_balance_page)
        asset_detail_operation_layout.addWidget(asset_operation_widget)
        balance_detail_operation_widget = QWidget()
        balance_detail_operation_widget.setLayout(asset_detail_operation_layout)


        balance_and_detail_layout = QHBoxLayout()
        balance_and_detail_layout.addWidget(self.balance_list_tableview)
        balance_and_detail_layout.addWidget(balance_detail_operation_widget)
        widget_balance = QWidget()
        widget_balance.setLayout(balance_and_detail_layout)

        return widget_balance


    def tab_is_selected(self, index):
        print("tab is changed" + str(index))
        if index == 0:
            self.update_balance()
        if index == 1:
            exin_worker = ExinPrice_Thread(mixin_asset_id_collection.USDT_ASSET_ID, "")
            exin_worker.signals.result.connect(self.received_exin_result)
            exin_worker.signals.finished.connect(self.exin_thread_complete)
            self.threadPool.start(exin_worker)

        if index == 3:
            self.update_transaction_history()
        if index == 4:

            self.total_node_label.setText("Loading...")
            mixin_node_info_thread = Mixin_node_info_Thread()
            mixin_node_info_thread.signals.result.connect(self.received_mixin_node_info_result)
            self.threadPool.start(mixin_node_info_thread)

        if index == 5:
            mixin_top_worker = MixinTopAsset_Thread()
            mixin_top_worker.signals.result.connect(self.received_mixin_top_result)
            self.threadPool.start(mixin_top_worker)

    def update_balance(self):
        worker = Balance_Thread(self.selected_wallet_record)
        worker.signals.result.connect(self.received_balance_result)
        worker.signals.finished.connect(self.balance_load_thread_complete)
        self.threadPool.start(worker)

    def open_selected_wallet(self):
        if (hasattr(self, "selected_wallet_record")):
            print("self.selected_wallet_record.userid is %s"%self.selected_wallet_record.userid)
            worker = Balance_Thread(self.selected_wallet_record)
            worker.signals.result.connect(self.received_balance_result)
            worker.signals.finished.connect(self.balance_load_thread_complete)

            user_profile_worker = UserProfile_Thread(self.selected_wallet_record)
            engine = sqlalchemy.create_engine('sqlite:///' + self.file_name + '.snapshot.db')
            # Create all tables in the engine. This is equivalent to "Create Table"
            # statements in raw SQL.
            mixin_sqlalchemy_type.Base.metadata.create_all(engine)
            mixin_sqlalchemy_type.Base.metadata.bind = engine
 
            DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
            self.session = DBSession()

            user_profile_worker.signals.result.connect(self.received_user_profile_result)
            user_profile_worker.signals.finished.connect(self.thread_complete)
            self.threadPool.start(worker)
            self.threadPool.start(user_profile_worker)

            self.widget_balance_widget = self.create_balance_widget()
            self.account_transaction_history_widget = self.open_transaction_history()
            self.account_transaction_history_widget.clicked.connect(self.transaction_record_selected)
            self.account_transaction_history_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

            self.transaction_statusBar = QStatusBar()
            self.the_last_snapshots_time = ""
            transaction_layout = QVBoxLayout()
            transaction_layout.addWidget(self.account_transaction_history_widget)
            transaction_layout.addWidget(self.transaction_statusBar)
            transaction_widget = QWidget()
            transaction_widget.setLayout(transaction_layout)
            self.transaction_record_explain_table = QTableView()
            transaction_history_detail_layout = QHBoxLayout()
            transaction_history_detail_layout.addWidget(transaction_widget)
            transaction_history_detail_layout.addWidget(self.transaction_record_explain_table)
            transaction_history_detail_widget = QWidget()
            transaction_history_detail_widget.setLayout(transaction_history_detail_layout)

            self.mixin_network_topasset_table = QTableView()
            self.mixin_network_fullnodes_table = QTableView()

            mixin_network_security_layer = QVBoxLayout()
            mixin_network_security_layer.addWidget(QLabel("Total mixin nodes:"))
            self.total_mixin_node_input = QLineEdit()
            self.total_mixin_node_input.textChanged.connect(self.mixin_node_change)
            mixin_network_security_layer.addWidget(self.total_mixin_node_input)

            self.total_asset_usd_value_exclude_xin_label = QLabel("")
            self.maximum_failed_node_mixin_label = QLabel("0")
            self.minimum_node_to_stop_mixin_label = QLabel("A")
            self.minimum_node_to_control_mixin_label = QLabel("B")
            mixin_network_security_layer.addWidget(self.maximum_failed_node_mixin_label)
            mixin_network_security_layer.addWidget(self.minimum_node_to_stop_mixin_label)
            mixin_network_security_layer.addWidget(self.minimum_node_to_control_mixin_label)
            mixin_network_security_layer.addWidget(self.total_asset_usd_value_exclude_xin_label)

            mixin_network_security_layer.addWidget(self.mixin_network_topasset_table)
            self.total_node_label = QLabel()


            mixin_network_status_layer = QVBoxLayout()

            mixin_network_status_layer.addWidget(self.total_node_label)
            mixin_network_status_layer.addWidget(self.mixin_network_fullnodes_table)
            mixin_network_security_widget = QWidget()
            mixin_network_security_widget.setLayout(mixin_network_security_layer)
            mixin_network_status_widget = QWidget()
            mixin_network_status_widget.setLayout(mixin_network_status_layer)
           

            self.exin_title_trade_list_detail = self.create_exin_exchange_widget()
            self.oceanone_title_trade_list_detail = self.create_ocean_exchange_widget()

            self.account_tab_widget = QTabWidget()
            self.account_tab_widget.addTab(self.widget_balance_widget, "Balance")
            self.account_tab_widget.addTab(self.exin_title_trade_list_detail, "Instant Exin Exchange")
            self.account_tab_widget.addTab(self.oceanone_title_trade_list_detail, "OceanOne exchange")
            self.account_tab_widget.addTab(transaction_history_detail_widget, "My transactions")

            self.account_tab_widget.addTab(mixin_network_status_widget, "Mixin Network status")
            self.account_tab_widget.addTab(mixin_network_security_widget, "Mixin Network threaten status")
            self.account_tab_widget.show()
            self.account_tab_widget.currentChanged.connect(self.tab_is_selected)
        else:
            return


app = QApplication([])
window = MainWindow()
app.exec_()

