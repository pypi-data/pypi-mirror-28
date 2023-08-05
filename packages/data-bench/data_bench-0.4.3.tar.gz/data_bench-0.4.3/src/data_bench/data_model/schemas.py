#
#   Copyright 2017 Intel Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#    
'''
'''

from collections import namedtuple

        
class Schemas(object):
    '''
    '''
    _maxAccounts = 10
    _maxSecurities = 18

    # XXX need a versioned schema
    
    _table_rows = {
        'AccountPermission': ['AP_CA_ID','AP_ACL', 'AP_TAX_ID',
                              'AP_F_NAME','AP_L_NAME'],
        'Address': ['AD_ID','AD_LINE1','AD_LINE2','AD_ZIP',
                    'AD_CTRY'], 
        'Broker': ['B_ID','B_ST_ID','B_NAME',
                   'B_NUM_TRADES','B_COMM_TOTAL'],
        'CashTransaction': ['CT_T_ID','CT_DTS','CT_AMT','CT_NAME'],
        'Charge': ['CH_TT_ID','CH_C_TIER','CH_CHRG'],
        'CommissionRate': ['CR_C_TIER','CR_TT_ID','CR_EX_ID',
                           'CR_FROM_QTY','CR_TO_QTY','CR_RATE'],
        'Company': ['CO_ID','CO_ST_ID','CO_NAME','CO_IN_ID',
                    'CO_SP_RATE','CO_CEO','CO_AD_ID','CO_DESC',
                    'CO_OPEN_DATE'],
        'CompanyCompetitor':['CP_CO_ID','CP_COMP_CO_ID','CP_IN_ID'],
        'Customer': ['C_ID','C_TAX_ID','C_ST_ID','C_L_NAME',
                     'C_F_NAME','C_M_NAME','C_GENDER','C_TIER',
                     'C_DOB','C_AD_ID','C_COUNTRY_1','C_AREA_1',
                     'C_LOCAL_1','C_EXT_1','C_COUNTRY_2','C_AREA_2',
                     'C_LOCAL_2','C_EXT_2','C_COUNTRY_3','C_AREA_3',
                     'C_LOCAL_3','C_EXT_3','C_EMAIL_1','C_EMAIL_2'],
        'CustomerAccount': ['CA_ID','CA_B_ID','CA_C_ID','CA_NAME',
                            'CA_TAX_ST','CA_BAL'],
        'CustomerAccount2': ['CA_C_ID','CA_ID','CA_TAX_ID',
                             'CA_B_ID','CA_NAME','CA_BAL',
                             'CA_L_NAME','CA_F_NAME','CA_M_NAME'],
        'CustomerTaxrate': ['CX_TX_ID','CX_C_ID'],
        'DailyMarket': ['DM_DATE','DM_S_SYMBOL','DM_CLOSE',
                        'DM_HIGH','DM_LOW','DM_VOL'],
        'Exchange': ['EX_ID','EX_NAME','EX_NUM_SYMBOL','EX_OPEN',
                     'EX_CLOSE','EX_DESC','EX_AD_ID'],
        'Financial': ['FI_CO_ID','FI_YEAR','FI_QTR',
                      'FI_QTR_START_DATE','FI_REVENUE',
                      'FI_NET_EARN','FI_BASIC_EPS',
                      'FI_DILUT_EPS','FI_MARGIN','FI_INVENTORY',
                      'FI_ASSETS','FI_LIABILITY','FI_OUT_BASIC',
                      'FI_OUT_DILUT'],
        'Holding': ['H_T_ID','H_CA_ID','H_S_SYMBOL','H_DTS',
                    'H_PRICE','H_QTY'],
        'HoldingHistory': ['HH_H_T_ID','HH_T_ID',
                           'HH_BEFORE_QTY','HH_AFTER_QTY'],
        'HoldingSummary': ['HS_CA_ID','HS_S_SYMBOL','HS_QTY'],
        'Industry': ['IN_ID','IN_NAME','IN_SC_ID'],
        'LastTrade': ['LT_S_SYMBOL','LT_DTS','LT_PRICE','LT_OPEN_PRICE',
                      'LT_VOL'],
        'NewsItem': ['NI_ID','NI_HEADLINE','NI_SUMMARY','NI_ITEM',
                     'NI_DTS','NI_SOURCE','NI_AUTHOR'],
        'NewsXref': ['NX_NI_ID','NX_CO_ID'],
        'Security': ['S_SYMBOL','S_ISSUE','S_ST_ID','S_NAME',
                     'S_EX_ID','S_CO_ID','S_NUM_OUT',
                     'S_START_DATE','S_EXCH_DATE','S_PE',
                     'S_52WK_HIGH','S_52WK_HIGH_DATE',
                     'S_52WK_LOW','S_52WK_LOW_DATE',
                     'S_DIVIDEND','S_YIELD'],
        'Settlement': ['SE_T_ID','SE_CASH_TYPE',
                       'SE_CASH_DUE_DATE','SE_AMT'],
        'StatusType': ['ST_ID','ST_NAME'],
        'TaxRate': ['TX_ID','TX_NAME','TX_RATE'],
        'Trade': ['T_ID','T_DTS','T_ST_ID','T_TT_ID','T_IS_CASH',
                  'T_S_SYMBOL','T_QTY','T_BID_PRICE','T_CA_ID',
                  'T_EXEC_NAME','T_TRADE_PRICE','T_CHRG','T_COMM',
                  'T_TAX','T_LIFO'],
        'TradeHistory': ['TH_T_ID','TH_DTS','TH_ST_ID'],
        'TradeRequest': ['TR_T_ID','TR_TT_ID','TR_S_SYMBOL',
                         'TR_QTY','TR_BID_PRICE','TR_B_ID'],
        'TradeType': ['TT_ID','TT_NAME','TT_IS_SELL','TT_IS_MRKT'],
        'WatchList': ['WI_WL_ID','WI_S_SYMBOL'],
        'Zipcode': ['ZC_CODE','ZC_TOWN','ZC_DIV'],
    }

    _txn_requests = {
        'CustomerValuationRequest': ['C_ID','C_TAX_ID'],
        'MarketStream': ['PRICE_QUOTE', 'TRADE_QTY', 'SYMBOL'],
    }

    _txn_responses = {
        'CustomerValuationResponse': ['CV_L_NAME','CV_F_NAME',
                                      'CV_M_NAME','CV_TOTAL_VAL'] +\
        [f'CV_ACCOUNT_{x}' for x in range(0, _maxAccounts)],
        'AccountValuation': ['AV_ACCOUNT_NUM',
                             'AV_ACCOUNT_ID',
                             'AV_ACCOUNT_NAME',
                             'AV_ACCOUNT_TOTAL_VAL',
                             'AV_ACCOUNT_CASH_BAL'] + \
        [f'AV_SYMBOL_{x}' for x in range(0, _maxSecurities)],
        'SecurityValuation': ['SV_SEC_SEQ',
                              'SV_SEC_NAME',
                              'SV_SEC_QTY',
                              'SV_SEC_LT_VALUE',
                              'SV_SEC_HOLDING_VALUE']
    }
    

    @classmethod
    def createFactory(cls, name, schema, sep):
        '''
        '''
        f = lambda s: s.sep.join([str(getattr(s,x)) for x in s._fields])
        factory = namedtuple(name, schema)
        factory.sep = sep
        factory.__str__ = f
        return factory
    

    @classmethod
    def tableRowKeys(cls):
        '''
        '''
        return list(cls._table_rows.keys())

    
    @classmethod
    def tableRowFactory(cls, name, sep='|'):
        '''
        '''
        return cls.createFactory(name, cls._table_rows[name], sep)

    
    @classmethod
    def transactionRequestKeys(cls):
        '''
        '''
        return list(cls._txn_requests)

    
    @classmethod
    def transactionRequestFactory(cls, name, sep='|'):
        '''
        '''

        return cls.createFactory(name, cls._txn_requests[name], sep)

    
    @classmethod
    def transactionResponseKeys(cls):
        '''
        '''
        return list(cls._txn_response)    


    @classmethod
    def transactionResponseFactory(cls, name, sep='|'):
        '''
        '''

        return cls.createFactory(name, cls._txn_responses[name], sep)





