"""
Copyright 2017 Government of Canada - Public Services and Procurement Canada - buyandsell.gc.ca

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from indy import agent, anoncreds, ledger, signus, pool, wallet, IndyError
from indy.error import ErrorCode
from von_agent.nodepool import NodePool
from von_agent.demo_agents import TrustAnchorAgent, SRIAgent, OrgBookAgent, BCRegistrarAgent
from von_agent.util import encode, revealed_attrs, ppjson, claims_for, prune_claims_json

import datetime
import pytest
import json


def claim_value_pair(plain):
    return [str(plain), encode(plain)]


#noinspection PyUnusedLocal
@pytest.mark.asyncio
async def test_agents_direct(
        pool_name,
        pool_genesis_txn_path,
        seed_trustee1,
        pool_genesis_txn_file,
        path_home):

    # 1. Open pool, init agents
    p = NodePool(pool_name, pool_genesis_txn_path)
    await p.open()
    assert p.handle

    tag = TrustAnchorAgent(
        p,
        seed_trustee1,
        'trustee_wallet',
        None,
        '127.0.0.1',
        8000,
        'api/v0')
    sag = SRIAgent(
        p,
        'SRI-Agent-0000000000000000000000',
        'sri-agent-wallet',
        None,
        '127.0.0.1',
        8001,
        'api/v0')
    pspcobag = OrgBookAgent(
        p,
        'PSPC-Org-Book-Agent-000000000000',
        'pspc-org-book-agent-wallet',
        None,
        '127.0.0.1',
        8002,
        'api/v0')
    bcobag = OrgBookAgent(
        p,
        'BC-Org-Book-Agent-00000000000000',
        'bc-org-book-agent-wallet',
        None,
        '127.0.0.1',
        8003,
        'api/v0')
    bcrag = BCRegistrarAgent(
        p,
        'BC-Registrar-Agent-0000000000000',
        'bc-registrar-agent-wallet',
        None,
        '127.0.0.1',
        8004,
        'api/v0')

    await tag.open()
    await sag.open()
    await pspcobag.open()
    await bcobag.open()
    await bcrag.open()

    # 2. Publish agent particulars to ledger if not yet present
    for ag in (tag, sag, pspcobag, bcobag, bcrag):
        if not json.loads(await tag.get_nym(ag.did)):
            await tag.send_nym(ag.did, ag.verkey)
        if not json.loads(await tag.get_endpoint(ag.did)):
            await ag.send_endpoint()

    nyms = {
        'tag': await tag.get_nym(tag.did),
        'sag': await tag.get_nym(sag.did),
        'pspcobag': await tag.get_nym(pspcobag.did),
        'bcobag': await tag.get_nym(bcobag.did),
        'bcrag': await tag.get_nym(bcrag.did)
    }
    endpoints = {
        'tag': await tag.get_endpoint(tag.did),
        'sag': await tag.get_endpoint(sag.did),
        'pspcobag': await tag.get_endpoint(pspcobag.did),
        'bcobag': await tag.get_endpoint(bcobag.did),
        'bcrag': await tag.get_endpoint(bcrag.did)
    }

    print('\n\n== 1 == nyms {}\nendpoints {}\n'.format(nyms, endpoints))

    for k in nyms:
        assert 'dest' in nyms[k]
    for k in endpoints:
        assert 'host' in endpoints[k]
        assert 'port' in endpoints[k]

    # 3. Publish schema to ledger if not yet present; get from ledger
    bc_schema_data = {
        'name': 'bc-reg',
        'version': '1.0',
        'attr_names': [
            'id',
            'busId',
            'orgTypeId',
            'jurisdictionId',
            'legalName',
            'effectiveDate',
            'endDate'
        ]
    }

    sri_schema_data = {
        'name': 'sri',
        'version': '1.0',
        'attr_names': [
            'legalName',
            'jurisdictionId',
            'sriRegDate'
        ]
    }

    try:
        await tag.get_schema(tag.did, 'Xxxx', 'X.x')  # Bad version number
    except IndyError as e:
        assert ErrorCode.LedgerInvalidTransaction == e.error_code

    bc_schema_json = await bcrag.get_schema(bcrag.did, bc_schema_data['name'], bc_schema_data['version'])  # may exist
    if not json.loads(bc_schema_json):
        bc_schema_json = await bcrag.send_schema(json.dumps(bc_schema_data))
    bc_schema_json = await bcrag.get_schema(
        bcrag.did,
        bc_schema_data['name'],
        bc_schema_data['version'])  # should exist now
    bc_schema = json.loads(bc_schema_json)
    assert bc_schema
    print('\n\n== 2.0 == BC SCHEMA {}'.format(ppjson(bc_schema)))

    sri_schema_json = await sag.get_schema(sag.did, sri_schema_data['name'], sri_schema_data['version'])  # may exist
    if not json.loads(sri_schema_json):
        sri_schema_json = await sag.send_schema(json.dumps(sri_schema_data))
    sri_schema_json = await sag.get_schema(
        sag.did,
        sri_schema_data['name'],
        sri_schema_data['version'])  # should exist now
    sri_schema = json.loads(sri_schema_json)
    assert sri_schema
    print('\n\n== 2.1 == SRI SCHEMA {}'.format(ppjson(sri_schema)))

    # 4. BC Registrar and SRI agents (as Issuers) create, store, and publish claim definitions to ledger
    # print('TAG DID {}'.format(tag.did))            # V4SG...
    # print('SAG DID {}'.format(sag.did))            # FaBA...
    # print('PSPCOBAG DID {}'.format(pspcobag.did))  # 45Ue...
    # print('BCOBAG DID {}'.format(bcobag.did))      # Rzra...
    # print('BCRAG DID {}'.format(bcrag.did))        # Q4zq...
    non_claim_def_json = await bcobag.get_claim_def(999999, bcrag.did)  # ought not exist
    assert not json.loads(non_claim_def_json)

    bc_claim_def_json = await bcrag.send_claim_def(bc_schema_json)
    bc_claim_def_json = await bcobag.get_claim_def(bc_schema['seqNo'], bcrag.did)  # ought to exist now

    sri_claim_def_json = await sag.send_claim_def(sri_schema_json)
    sri_claim_def_json = await pspcobag.get_claim_def(sri_schema['seqNo'], sag.did)

    assert json.loads(bc_claim_def_json)['ref'] == bc_schema['seqNo']
    assert json.loads(sri_claim_def_json)['ref'] == sri_schema['seqNo']

    print('\n\n== 3.0 == BC claim def {}'.format(ppjson(json.loads(bc_claim_def_json))))
    print('\n\n== 3.1 == SRI claim def {}'.format(ppjson(json.loads(sri_claim_def_json))))

    # 5. Setup master secrets, claim reqs at HolderProver agents
    await bcobag.create_master_secret('MasterSecret')
    await pspcobag.create_master_secret('SecretMaster')

    for ag in (bcobag, pspcobag):
        wallet_num = ag.wallet.num
        assert (await ag.reset_wallet()) > wallet_num  # makes sure later ops are OK on reset wallet

    await bcobag.store_claim_offer(bcrag.did, bc_schema['seqNo'])
    bc_claim_req_json = await bcobag.store_claim_req(bcrag.did, bc_claim_def_json)
    print('\n\n== 4.0 == BC reg claim req {}'.format(ppjson(bc_claim_req_json)))

    await pspcobag.store_claim_offer(sag.did, sri_schema['seqNo'])
    sri_claim_req_json = await pspcobag.store_claim_req(sag.did, sri_claim_def_json)
    print('\n\n== 4.1 == SRI reg claim req {}'.format(ppjson(sri_claim_req_json)))

    # 6. BC Reg agent (as Issuer) issues claims and stores at HolderProver: get claim req, create claim, store claim
    bc_claims = [
        {
            'id': claim_value_pair('1'),
            'busId': claim_value_pair('11121398'),
            'orgTypeId': claim_value_pair('2'),
            'jurisdictionId': claim_value_pair('1'),
            'legalName': claim_value_pair('The Original House of Pies'),
            'effectiveDate': claim_value_pair('2010-10-10'),
            'endDate': claim_value_pair(None)
        },
        {
            'id': claim_value_pair('2'),
            'busId': claim_value_pair('11133333'),
            'orgTypeId': claim_value_pair('1'),
            'jurisdictionId': claim_value_pair('1'),
            'legalName': claim_value_pair('Planet Cake'),
            'effectiveDate': claim_value_pair('2011-10-01'),
            'endDate': claim_value_pair(None)
        },
        {
            'id': claim_value_pair('3'),
            'busId': claim_value_pair('11144444'),
            'orgTypeId': claim_value_pair('2'),
            'jurisdictionId': claim_value_pair('1'),
            'legalName': claim_value_pair('Tart City'),
            'effectiveDate': claim_value_pair('2012-12-01'),
            'endDate': claim_value_pair(None)
        }
    ]
    for c in bc_claims:
        (_, bc_claim_json) = await bcrag.create_claim(bc_claim_req_json, c)
        assert json.loads(bc_claim_json)
        await bcobag.store_claim(bc_claim_json)

    # 7. BC Org Book agent (as HolderProver) finds claims
    bc_by_attr = {
        'nonce': '1234',
        'name': 'bc_proof_req',
        'version': '0',
        'requested_attrs': {
            '{}_uuid'.format(attr): {
                'schema_seq_no': bc_schema['seqNo'],
                'name': attr
            } for attr in bc_claims[0]
        },
        'requested_predicates': {
        }
    } 
    (bc_claim_uuids_all, bc_claims_found_json) = await bcobag.get_claims(json.dumps(bc_by_attr))
    print('\n\n== 5 == BC claims by attr, no filter {}; {}'.format(bc_claim_uuids_all, ppjson(bc_claims_found_json)))
    bc_claims_found = json.loads(bc_claims_found_json)
    bc_display_pruned_postfilt = claims_for(bc_claims_found, {'legalName': bc_claims[2]['legalName'][0]})
    print('\n\n== 6 == display BC claims filtered post-hoc matching {}: {}'.format(
        bc_claims[2]['legalName'][0],
        ppjson(bc_display_pruned_postfilt)))
    bc_display_pruned = prune_claims_json({k for k in bc_display_pruned_postfilt}, bc_claims_found)
    print('\n\n== 7 == BC claims, stripped down {}'.format(ppjson(bc_display_pruned)))

    filter_enc = {k: bc_claims[2][k][0] for k in bc_claims[2] if k in ('jurisdictionId', 'busId')}
    (bc_claim_uuids_filt, bc_claims_found_json) = await bcobag.get_claims(json.dumps(bc_by_attr), filter_enc)
    print('\n\n== 8 == BC claims by attr, filtered a priori {}; {}'.format(
        bc_claim_uuids_filt,
        ppjson(bc_claims_found_json)))
    assert set([*bc_display_pruned_postfilt]) == bc_claim_uuids_filt
    assert len(bc_display_pruned_postfilt) == 1

    bc_claim_uuid = bc_claim_uuids_filt.pop()

    # 8. BC Org Book (as HolderProver) creates proof for claim specified by filter
    bc_claims_found = json.loads(bc_claims_found_json)
    bc_requested_claims = {
        'self_attested_attributes': {},
        'requested_attrs': {
            attr: [bc_claim_uuid, True]
                for attr in bc_by_attr['requested_attrs'] if attr in bc_claims_found['attrs']
        },
        'requested_predicates': {
            pred: bc_claim_uuid
                for pred in bc_by_attr['requested_predicates']
        }
    }
    bc_proof_json = await bcobag.create_proof(
        json.dumps(bc_by_attr),
        bc_schema,
        json.loads(bc_claim_def_json),
        bc_requested_claims)
    print('\n\n== 9 == BC proof (by filter) {}'.format(ppjson(bc_proof_json)))

    # 9. SRI agent (as Verifier) verifies proof (by filter)
    rc_json = await sag.verify_proof(
        json.dumps(bc_by_attr),
        json.loads(bc_proof_json),
        bc_schema,
        json.loads(bc_claim_def_json))
    print('\n\n== 10 == The SRI agent verifies the BC proof (by filter) as {}'.format(ppjson(rc_json)))
    assert json.loads(rc_json)

    # 10. BC Org Book (as HolderProver) finds claim by claim-uuid, no claim by non-claim-uuid
    bc_claim_found_by_uuid = json.loads(await bcobag.get_claim_by_claim_uuid(bc_schema_json, bc_claim_uuid))
    print('\n\n== 11 == BC claim by claim-uuid={}: {}'.format(
        bc_claim_uuid,
        ppjson(bc_claim_found_by_uuid)))
    assert bc_claim_found_by_uuid
    assert bc_claim_found_by_uuid['attrs']

    bc_non_claim_by_uuid = json.loads(await bcobag.get_claim_by_claim_uuid(
        bc_schema_json,
        'claim::ffffffff-ffff-ffff-ffff-ffffffffffff'))
    print('\n\n== 12 == BC non-claim: {}'.format(ppjson(bc_non_claim_by_uuid)))
    assert bc_non_claim_by_uuid
    assert all(not bc_non_claim_by_uuid['attrs'][attr] for attr in bc_non_claim_by_uuid['attrs'])

    # 11. BC Org Book (as HolderProver) creates proof for claim specified by claim-uuid
    bc_requested_claims = {
        'self_attested_attributes': {},
        'requested_attrs': {
            attr: [bc_claim_uuid, True]
                for attr in bc_claim_found_by_uuid['attrs']
        },
        'requested_predicates': {
        }
    }
    bc_proof_json = await bcobag.create_proof(
        json.dumps(bc_by_attr),
        bc_schema,
        json.loads(bc_claim_def_json),
        bc_requested_claims)
    bc_proof = json.loads(bc_proof_json)
    print('\n\n== 13 == BC proof by claim-uuid={} {}'.format(bc_claim_uuid, ppjson(bc_proof_json)))

    # 12. SRI agent (as Verifier) verifies proof
    rc_json = await sag.verify_proof(
        json.dumps(bc_by_attr),
        bc_proof,
        bc_schema,
        json.loads(bc_claim_def_json))
    print('\n\n== 14 == BC proof by claim-uuid={} verifies as {}'.format(bc_claim_uuid, ppjson(rc_json)))
    assert json.loads(rc_json)

    # 13. Create and store SRI registration completion claim from verified proof
    revealed = revealed_attrs(bc_proof)
    sri_claim = {k: claim_value_pair(revealed[k]) for k in revealed if k in sri_schema_data['attr_names']}
    yyyy_mm_dd = datetime.date.today().strftime('%Y-%m-%d')
    sri_claim['sriRegDate'] = claim_value_pair(yyyy_mm_dd)
    print('\n\n== 15 == SRI claim: {}'.format(ppjson(sri_claim)))
    (_, sri_claim_json) = await sag.create_claim(sri_claim_req_json, sri_claim)
    assert json.loads(sri_claim_json)
    await pspcobag.store_claim(sri_claim_json)

    # 14. PSPC Org Book Agent (as HolderProver) finds claim
    sri_by_attr = {
        'nonce': '9999',
        'name': 'sri_proof_req',
        'version': '0',
        'requested_attrs': {
            '{}_uuid'.format(attr): {
                'schema_seq_no': sri_schema['seqNo'],
                'name': attr
            } for attr in sri_claim
        },
        'requested_predicates': {
        }
    } 

    (sri_claim_uuids_all, sri_claims_found_json) = await pspcobag.get_claims(json.dumps(sri_by_attr))
    print('\n\n== 16 == SRI claims by attr, no filter {}; {}'.format(
        sri_claim_uuids_all,
        ppjson(sri_claims_found_json)))
    assert len(sri_claim_uuids_all) == 1
    sri_claim_uuid = sri_claim_uuids_all.pop()
    sri_claims_found = json.loads(sri_claims_found_json)

    # 15. PSPC Org Book Agent (as HolderProver) creates proof
    sri_requested_claims = {
        'self_attested_attributes': {},
        'requested_attrs': {
            attr: [sri_claim_uuid, True]
                for attr in sri_claims_found['attrs']
        },
        'requested_predicates': {
        }
    }
    sri_proof_json = await pspcobag.create_proof(
        json.dumps(sri_by_attr),
        sri_schema,
        json.loads(sri_claim_def_json),
        sri_requested_claims)
    print('\n\n== 17 == PSPC Org Book proof on claim-uuid={} {}'.format(sri_claim_uuid, ppjson(sri_proof_json)))

    # 16. SRI (as Verifier) verify proof
    rc_json = await sag.verify_proof(
        json.dumps(sri_by_attr),
        json.loads(sri_proof_json),
        sri_schema,
        json.loads(sri_claim_def_json))
    print('\n\n== 18 == the SRI agent verifies the PSPC Org Book proof by claim-uuid={} as {}'.format(
        sri_claim_uuid,
        ppjson(rc_json)))
    assert json.loads(rc_json)

    await bcrag.close()
    await bcobag.close()
    await pspcobag.close()
    await sag.close()
    await tag.close()
    await p.close()


#noinspection PyUnusedLocal
@pytest.mark.asyncio
async def test_agents_process_forms_local(
        pool_name,
        pool_genesis_txn_path,
        seed_trustee1,
        pool_genesis_txn_file,
        path_home):

    # 1. Open pool, init agents
    async with NodePool(pool_name, pool_genesis_txn_path) as p, (
            TrustAnchorAgent(
                p,
                seed_trustee1,
                'trustee_wallet',
                None,
                '127.0.0.1',
                '8000',
                'api/v0')) as tag, (
            SRIAgent(
                p,
                'SRI-Agent-0000000000000000000000',
                'sri-agent-wallet',
                None,
                '127.0.0.1',
                8001,
                'api/v0')) as sag, (
            OrgBookAgent(
                p,
                'PSPC-Org-Book-Agent-000000000000',
                'pspc-org-book-agent-wallet',
                None,
                '127.0.0.1',
                8003,
                'api/v0')) as pspcobag, (
            OrgBookAgent(
                p,
                'BC-Org-Book-Agent-00000000000000',
                'bc-org-book-agent-wallet',
                None,
                '127.0.0.1',
                8003,
                'api/v0')) as bcobag, (
            BCRegistrarAgent(
                p,
                'BC-Registrar-Agent-0000000000000',
                'bc-reg-agent-wallet',
                None,
                '127.0.0.1',
                8004,
                'api/v0')) as bcrag:

        assert p.handle is not None

        # 2. Publish agent particulars to ledger if not yet present
        for ag in (tag, sag, pspcobag, bcobag, bcrag):
            nym_lookup_form = {
                'type': 'agent-nym-lookup',
                'data': {
                    'agent-nym': {
                        'did': ag.did
                    }
                }
            }
            nym = json.loads(await ag.process_post(nym_lookup_form))
            if not nym:
                resp_json = await tag.process_post({
                    'type': 'agent-nym-send',
                    'data': {
                        'agent-nym': {
                            'did': ag.did,
                            'verkey': ag.verkey
                        }
                    }
                })

            nym = json.loads(await ag.process_post(nym_lookup_form))
            assert nym

            endpoint_lookup_form = {
                'type': 'agent-endpoint-lookup',
                'data': {
                    'agent-endpoint': {
                        'did': ag.did
                    }
                }
            }
            endpoint = json.loads(await tag.process_post(endpoint_lookup_form))
            if not endpoint:
                resp_json = await ag.process_post({
                    'type': 'agent-endpoint-send',
                    'data': {
                    }
                })
            endpoint = json.loads(await ag.process_post(endpoint_lookup_form))
            assert endpoint

        try:  # Make sure only a trust anchor can register an agent
            await sag.process_post({
                'type': 'agent-nym-send',
                'data': {
                    'agent-nym': {
                        'did': sag.did,
                        'verkey': sag.verkey
                    }
                }
            })
            assert False
        except NotImplementedError:
            pass

        # 3. Publish schema to ledger if not yet present; get from ledger
        bc_schema_data = {
            'name': 'bc-reg',
            'version': '1.0',
            'attr_names': [
                'id',
                'busId',
                'orgTypeId',
                'jurisdictionId',
                'legalName',
                'effectiveDate',
                'endDate'
            ]
        }

        bc_schema_lookup_form = {
            'type': 'schema-lookup',
            'data': {
                'schema': {
                    'origin-did': bcrag.did,
                    'name': bc_schema_data['name'],
                    'version': 'xxxx'
                }
            }
        }

        sri_schema_data = {
            'name': 'sri',
            'version': '1.0',
            'attr_names': [
                'legalName',
                'jurisdictionId',
                'sriRegDate'
            ]
        }

        sri_schema_lookup_form = {
            'type': 'schema-lookup',
            'data': {
                'schema': {
                    'origin-did': sag.did,
                    'name': sri_schema_data['name'],
                    'version': sri_schema_data['version']
                }
            }
        }

        try:
            schema_json = await bcrag.process_post(bc_schema_lookup_form)  # Bad version number
            assert False
        except IndyError:
            pass

        bc_schema_lookup_form['data']['schema']['version'] = '999.999'
        assert not json.loads(await bcrag.process_post(bc_schema_lookup_form))  # ought not exist
        bc_schema_lookup_form['data']['schema']['version'] = '1.0'
        bc_schema_json = await bcrag.process_post(bc_schema_lookup_form)  # may exist
        if not json.loads(bc_schema_json):
            bc_schema_send = json.loads(await bcrag.process_post({
                'type': 'schema-send',
                'data': {
                    'schema': {
                        'origin-did': bcrag.did,
                        'name': bc_schema_data['name'],
                        'version': bc_schema_data['version']
                    },
                    'attr-names': bc_schema_data['attr_names']
                }
            }))
            assert bc_schema_send
        bc_schema_json = await bcrag.process_post(bc_schema_lookup_form)
        bc_schema = json.loads(bc_schema_json)  # should exist now
        assert bc_schema
        print('\n\n== 2 == BC SCHEMA {}'.format(ppjson(bc_schema)))

        for ag in (pspcobag, bcobag):
            try:  # Make sure only an origin can send a schema
                await ag.process_post({
                    'type': 'schema-send',
                    'data': {
                        'schema': {
                            'origin-did': ag.did,
                            'name': bc_schema_data['name'],
                            'version': bc_schema_data['version']
                        },
                        'attr-names': bc_schema_data['attr_names']
                    }
                })
                assert False
            except NotImplementedError:
                pass

        # 4. BC Registrar and SRI agents (as Issuers) create, store,  and publish claim def to ledger
        # print('TAG DID {}'.format(tag.did))            # V4SG...
        # print('SAG DID {}'.format(sag.did))            # FaBA...
        # print('PSPCOBAG DID {}'.format(pspcobag.did))  # 45Ue...
        # print('BCOBAG DID {}'.format(bcobag.did))      # Rzra...
        # print('BCRAG DID {}'.format(bcrag.did))        # Q4zq...

        bc_claim_def_send_form = {
            'type': 'claim-def-send',
            'data': {
                'schema': {
                    'origin-did': bcrag.did,
                    'name': bc_schema_data['name'],
                    'version': bc_schema_data['version']
                }
            }
        }

        await bcrag.process_post(bc_claim_def_send_form)
        bc_claim_def_json = await bcobag.get_claim_def(
            bc_schema['seqNo'],
            bcrag.did)  # ought to exist now (short-circuit to low-level API)
        assert json.loads(bc_claim_def_json)['ref'] == bc_schema['seqNo']

        # 5. Setup master secrets, claim reqs at HolderProver agents
        master_secret_set_form = {
            'type': 'master-secret-set',
            'data': {
                'label': 'maestro'
            }
        }
        bc_claim_hello_form = {
            'type': 'claim-hello',
            'data': {
                'issuer-did': bcrag.did
            }
        }

        try:  # master secret unspecified, ought to fail
            await bcobag.process_post(bc_claim_hello_form)
        except ValueError:
            pass

        await bcobag.process_post(master_secret_set_form)

        try:  # schema unspecified, ought to fail
            bc_claim_req_json = await bcobag.process_post(bc_claim_hello_form)
        except ValueError:
            pass

        claims_reset_form = {
            'type': 'claims-reset',
            'data': {
            }
        }
        claims_reset_resp = json.loads(await bcobag.process_post(claims_reset_form))
        assert not claims_reset_resp  # make sure later ops are OK on reset wallet -- response is {} if OK

        bc_claim_hello_form['data']['schema'] = {
            'origin-did': bcrag.did,
            'name': bc_schema_data['name'],
            'version': bc_schema_data['version']
        }
        bc_claim_req_json = await bcobag.process_post(bc_claim_hello_form)
        bc_claim_req = json.loads(bc_claim_req_json)
        assert bc_claim_req

        # 6. BC Reg agent (as Issuer) issues claims and stores at HolderProver: get claim req, create claim, store claim
        bc_claims = [
            {
                'id': 1,
                'busId': 11121398,
                'orgTypeId': 2,
                'jurisdictionId': 1,
                'legalName': 'The Original House of Pies',
                'effectiveDate': '2010-10-10',
                'endDate': None
            },
            {
                'id': 2,
                'busId': 11133333,
                'orgTypeId': 1,
                'jurisdictionId': 1,
                'legalName': 'Planet Cake',
                'effectiveDate': '2011-10-01',
                'endDate': None
            },
            {
                'id': 3,
                'busId': 11144444,
                'orgTypeId': 2,
                'jurisdictionId': 1,
                'legalName': 'Tart City',
                'effectiveDate': '2012-12-01',
                'endDate': None
            }
        ]
        for c in bc_claims:
            bc_claim_json = await bcrag.process_post({
                'type': 'claim-create',
                'data': {
                    'claim-req': bc_claim_req,
                    'claim-attrs': c
                }
            })
            await bcobag.process_post({
                'type': 'claim-store',
                'data': {
                    'claim': json.loads(bc_claim_json)
                }
            })

        # 7. BC Org Book agent (as HolderProver) finds claims
        bc_by_attr = {
            'nonce': '1234',
            'name': 'proof_req',
            'version': '0',
            'requested_attrs': {
                '{}_uuid'.format(attr): {
                    'schema_seq_no': bc_schema['seqNo'],
                    'name': attr
                } for attr in bc_claims[0]
            },
            'requested_predicates': {
            },
        } 
        bc_claims_all = json.loads(await bcobag.process_post({
            'type': 'claim-request',
            'data': {
                'schema': {
                    'origin-did': bcrag.did,
                    'name': bc_schema_data['name'],
                    'version': bc_schema_data['version']
                },
                'claim-filter': {
                    'attr-match': {
                    },
                    'predicate-match': [
                    ]
                }
            }
        }))
        print('\n\n== 3 == BC claims by attr, no filter, process-post {}'.format(ppjson(bc_claims_all)))
        bc_display_pruned_postfilt = claims_for(bc_claims_all['claims'], {'legalName': bc_claims[2]['legalName']})
        print('\n\n== 4 == display BC claims filtered post-hoc matching {}: {}'.format(
            bc_claims[2]['legalName'],
            ppjson(bc_display_pruned_postfilt)))
        bc_display_pruned = prune_claims_json({k for k in bc_display_pruned_postfilt}, bc_claims_all['claims'])
        print('\n\n== 5 == BC claims, stripped down {}'.format(ppjson(bc_display_pruned)))

        bc_claims_prefilt_json = await bcobag.process_post({
            'type': 'claim-request',
            'data': {
                'schema': {
                    'origin-did': bcrag.did,
                    'name': bc_schema_data['name'],
                    'version': bc_schema_data['version']
                },
                'claim-filter': {
                    'attr-match': {
                        k: bc_claims[2][k] for k in bc_claims[2] if k in ('jurisdictionId', 'busId')
                    },
                    'predicate-match': [
                    ]
                }
            }
        })
        bc_claims_prefilt = json.loads(bc_claims_prefilt_json)
        print('\n\n== 6 == BC claims by attr, with filter a priori, process-post {}'.format(ppjson(bc_claims_prefilt)))
        bc_display_pruned_prefilt = claims_for(bc_claims_prefilt['claims'])
        print('\n\n== 7 == BC display claims filtered a priori matching {}: {}'.format(
            bc_claims[2]['legalName'],
            ppjson(bc_display_pruned_prefilt)))
        assert set([*bc_display_pruned_postfilt]) == set([*bc_display_pruned_prefilt])
        assert len(bc_display_pruned_postfilt) == 1

        # 8. BC Org Book (as HolderProver) creates proof (by filter)
        bc_proof_resp = json.loads(await bcobag.process_post({
            'type': 'proof-request',
            'data': {
                'schema': {
                    'origin-did': bcrag.did,
                    'name': bc_schema_data['name'],
                    'version': bc_schema_data['version']
                },
                'claim-filter': {
                    'attr-match': {
                        k: bc_claims[2][k] for k in bc_claims[2] if k in ('jurisdictionId', 'busId')
                    },
                    'predicate-match': [
                    ]
                }
            }
        }))
        print('\n\n== 8 == BC proof response (by filter) {}'.format(ppjson(bc_proof_resp)))

        # 9. SRI agent (as Verifier) verifies proof (by filter)
        rc_json = await sag.process_post({
            'type': 'verification-request',
            'data': {**bc_proof_resp,
                'schema': {
                    'origin-did': bcrag.did,
                    'name': bc_schema_data['name'],
                    'version': bc_schema_data['version']
                }
            }
        })
        print('\n\n== 9 == the SRI agent verifies the BC proof (by filter) as {}'.format(ppjson(rc_json)))
        assert json.loads(rc_json)

        # 10. BC Org Book (as HolderProver) creates proof (by claim-uuid)
        bc_claim_uuid = set([*bc_display_pruned_prefilt]).pop()
        bc_proof_resp = json.loads(await bcobag.process_post({
            'type': 'proof-request-by-claim-uuid',
            'data': {
                'schema': {
                    'origin-did': bcrag.did,
                    'name': bc_schema_data['name'],
                    'version': bc_schema_data['version']
                },
                'claim-uuid': bc_claim_uuid
            }
        }))
        print('\n\n== 10 == BC proof response by claim-uuid={}: {}'.format(bc_claim_uuid, ppjson(bc_proof_resp)))

        # 11. BC Org Book (HolderProver) creates non-proof (by non-claim-uuid)
        bc_non_claim_uuid = 'claim::ffffffff-ffff-ffff-ffff-ffffffffffff'
        try:
            json.loads(await bcobag.process_post({
                'type': 'proof-request-by-claim-uuid',
                'data': {
                    'schema': {
                        'origin-did': bcrag.did,
                        'name': bc_schema_data['name'],
                        'version': bc_schema_data['version']
                    },
                    'claim-uuid': bc_non_claim_uuid
                }
            }))
            assert False
        except ValueError:
            pass

        # 12. SRI agent (as Verifier) verifies proof (by claim-uuid)
        rc_json = await sag.process_post({
            'type': 'verification-request',
            'data': {**bc_proof_resp,
                'schema': {
                    'origin-did': bcrag.did,
                    'name': bc_schema_data['name'],
                    'version': bc_schema_data['version']
                }
            }
        })
        print('\n\n== 12 == SRI agent verifies BC proof by claim_uuid={} as {}'.format(
            bc_claim_uuid,
            ppjson(rc_json)))
        assert json.loads(rc_json)

        # 13. Finish bootstrapping SRI agent as Origin and Issuer, PSPC Org Book agent as HolderProver
        sri_schema_json = await sag.process_post(sri_schema_lookup_form)  # may exist
        if not json.loads(sri_schema_json):
            sri_schema_send = json.loads(await sag.process_post({
                'type': 'schema-send',
                'data': {
                    'schema': {
                        'origin-did': sag.did,
                        'name': sri_schema_data['name'],
                        'version': sri_schema_data['version']
                    },
                    'attr-names': sri_schema_data['attr_names']
                }
            }))
            assert bc_schema_send
        sri_schema_json = await sag.process_post(sri_schema_lookup_form)
        sri_schema = json.loads(sri_schema_json)  # should exist now
        assert sri_schema
        print('\n\n== 13 == SRI SCHEMA {}'.format(ppjson(sri_schema)))

        sri_claim_def_send_form = {
            'type': 'claim-def-send',
            'data': {
                'schema': {
                    'origin-did': sag.did,
                    'name': sri_schema_data['name'],
                    'version': sri_schema_data['version']
                }
            }
        }

        await sag.process_post(sri_claim_def_send_form)
        sri_claim_def_json = await pspcobag.get_claim_def(
            sri_schema['seqNo'],
            sag.did)  # ought to exist now (short-circuit to low-level API)
        assert json.loads(sri_claim_def_json)['ref'] == sri_schema['seqNo']

        master_secret_set_form['data']['label'] = 'shhhh'
        await pspcobag.process_post(master_secret_set_form)
        sri_claims_reset_resp = json.loads(await pspcobag.process_post(claims_reset_form))
        assert not sri_claims_reset_resp  # make sure later ops are OK on reset wallet -- response is {} if OK

        # 14. Create and store SRI registration completion claim from verified proof
        sri_claim_hello_form = {
            'type': 'claim-hello',
            'data': {
                'issuer-did': sag.did,
                'schema': {
                    'origin-did': sag.did,
                    'name': sri_schema_data['name'],
                    'version': sri_schema_data['version']
                }
            }
        }
        sri_claim_req_json = await pspcobag.process_post(sri_claim_hello_form)
        sri_claim_req = json.loads(sri_claim_req_json)
        assert sri_claim_req

        revealed = revealed_attrs(bc_proof_resp['proof'])
        sri_claim = {k: claim_value_pair(revealed[k]) for k in revealed if k in sri_schema_data['attr_names']}
        yyyy_mm_dd = datetime.date.today().strftime('%Y-%m-%d')
        sri_claim['sriRegDate'] = claim_value_pair(yyyy_mm_dd)
        print('\n\n== 14 == sri_claim: {}'.format(ppjson(sri_claim)))

        sri_claim_json = await sag.process_post({
            'type': 'claim-create',
            'data': {
                'claim-req': sri_claim_req,
                'claim-attrs': sri_claim
            }
        })
        await pspcobag.process_post({
            'type': 'claim-store',
            'data': {
                'claim': json.loads(sri_claim_json)
            }
        })
        assert json.loads(sri_claim_json)

        # 15. PSPC Org Book (as HolderProver) finds claim
        sri_claims_all = json.loads(await pspcobag.process_post({
            'type': 'claim-request',
            'data': {
                'schema': {
                    'origin-did': sag.did,
                    'name': sri_schema_data['name'],
                    'version': sri_schema_data['version']
                },
                'claim-filter': {
                    'attr-match': {
                    },
                    'predicate-match': [
                    ]
                }
            }
        }))
        print('\n\n== 15 == SRI claim {}'.format(ppjson(sri_claims_all)))

        # 16. PSPC Org Book (as HolderProver) creates proof
        sri_display = claims_for(sri_claims_all['claims'])
        sri_claim_uuid = set([*sri_display]).pop()
        sri_proof_resp = json.loads(await pspcobag.process_post({
            'type': 'proof-request-by-claim-uuid',
            'data': {
                'schema': {
                    'origin-did': sag.did,
                    'name': sri_schema_data['name'],
                    'version': sri_schema_data['version']
                },
                'claim-uuid': sri_claim_uuid
            }
        }))
        print('\n\n== 16 == SRI proof response by claim-uuid={}: {}'.format(sri_claim_uuid, ppjson(sri_proof_resp)))

        # 17. SRI (as Verifier) verifies proof
        rc_json = await sag.process_post({
            'type': 'verification-request',
            'data': {**sri_proof_resp,
                'schema': {
                    'origin-did': sag.did,
                    'name': sri_schema_data['name'],
                    'version': sri_schema_data['version']
                }
            }
        })
        print('\n\n== 17 == SRI agent verifies SRI proof by claim_uuid={} as {}'.format(
            sri_claim_uuid,
            ppjson(rc_json)))
        assert json.loads(rc_json)

        # 18. Exercise helper GET calls
        txn_json = await sag.process_get_txn(sri_schema['seqNo'])
        print('\n\n== 18 == SRI schema by txn #{}: {}'.format(sri_schema['seqNo'], ppjson(txn_json)))
        assert json.loads(txn_json)
        txn_json = await sag.process_get_txn(99999)  # ought not exist
        assert not json.loads(txn_json)

        did_json = await bcrag.process_get_did()
        print('\n\n== 19 == BC Registrar agent did: {}'.format(ppjson(did_json)))
        assert json.loads(did_json)
