export interface ActionDto {
  domain: {
    config: any;
    session_config: any;
    intents: [];
    entities: [];
    slots: any;
    responses: any;
    actions: [];
    forms: any;
    e2e_actions: [];
  };
  next_action: string;
  tracker: {
    sender_id: string;
    slots: { session_started_metadata: [] };
    latest_message: {
      intent: any;
      entities: Array<{
        entity: string;
        value: string;
      }>;
      text: string;
      message_id: string;
      metadata: any;
      intent_ranking: [];
      response_selector: any;
    };
    latest_event_time: number;
    followup_action: any;
    paused: boolean;
    events: [];
    latest_input_channel: string;
    active_loop: any;
    latest_action: { action_name: string };
    latest_action_name: string;
  };
  sender_id: string;
  version: string;
}
