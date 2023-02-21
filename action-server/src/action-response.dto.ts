export interface ActionResponseDto {
  events: Array<{
    event:
      | 'slot'
      | 'reset_slots'
      | 'bot'
      | 'reminder'
      | 'cancel_reminder'
      | 'pause'
      | 'resume'
      | 'undo'
      | 'restart'
      | 'session_started';
    text?: string;
    data?: any;
    name?: string;
    value?: any;
  }>;
  responses?: [];
}
