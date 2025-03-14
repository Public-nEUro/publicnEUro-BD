/**
 * Usage API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { Acceptance } from './acceptance';


export interface InstitutionWithAcceptance { 
    contact: string;
    country_id: string | null;
    has_rejected_all_sccs: boolean;
    id: string;
    name: string;
    scc_acceptance: { [key: string]: Acceptance; };
}

